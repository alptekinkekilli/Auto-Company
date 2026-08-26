#!/usr/bin/env python3
"""SessionStart hook: keep the git-tracked graft cards fresh, threshold-gated.

`./.graft-kit/bin/graft-build.sh --deep` is PAID (Together API) and takes minutes, so
it must not run on every session — only when the cards are genuinely behind. This hook
measures freshness from git (there is no external artifact store in this project; the
"deep artifact" is the versioned `graft/*.md` cards), and when a DOUBLE threshold is
crossed it launches the deep build in the background (nohup) and returns immediately.

Design (adapted from an operator-supplied reference plan proven in another project):
- Double threshold: commits-behind > MAX_BEHIND AND last-graft-commit age > MAX_AGE_H.
  Either alone is not enough — a busy hour or a quiet day should not trigger a paid run.
- Fail-open, ALWAYS exit 0: a git/npx/lock error must never block session start or compact.
- Non-blocking: the deep build runs detached; this hook prints one line and exits.
- The Together API key never touches this script — graft-build.sh reads it from Keychain.

stdout is one line and lands in the session-brief context, so the operator sees graft
freshness every session. It also writes logs/graft-freshness.json for the cockpit.

  graft-auto-refresh.py            # check + maybe launch, one-line stdout
  graft-auto-refresh.py --dry-run  # compute + write freshness.json, NEVER launch
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Thresholds — this project's single source of truth (no external watchdog here).
# Loosen via env, never by editing code, so the cockpit/hook stay in agreement.
MAX_BEHIND = int(os.environ.get("GRAFT_MAX_BEHIND", "40"))
MAX_AGE_H = float(os.environ.get("GRAFT_MAX_AGE_H", "24"))
RELAUNCH_WINDOW_S = 30 * 60  # covers the lock race + a ~25-min run window

DRY_RUN = "--dry-run" in sys.argv[1:]


def _repo_root() -> Path | None:
    here = Path(__file__).resolve().parent
    try:
        out = subprocess.run(
            ["git", "-C", str(here), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=10,
            env={**os.environ, "LC_ALL": "C"},
        )
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip())
    except Exception:
        pass
    return None


def _git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, timeout=15,
            env={**os.environ, "LC_ALL": "C"},
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return None


def _lock_alive(lock: Path) -> int | None:
    """Return the live pid holding the lock, or None (missing/stale)."""
    try:
        pid = int(lock.read_text().strip())
    except Exception:
        return None
    try:
        os.kill(pid, 0)  # signal 0 = existence check
        return pid
    except (OSError, ProcessLookupError):
        return None  # stale lock, process gone


def _emit(line: str, status: dict, root: Path | None) -> None:
    """One line to stdout; best-effort freshness.json for the cockpit; exit 0."""
    print(line)
    if root is not None:
        try:
            fresh = root / "logs" / "graft-freshness.json"
            fresh.parent.mkdir(parents=True, exist_ok=True)
            fresh.write_text(json.dumps(status, ensure_ascii=False))
        except Exception:
            pass
    sys.exit(0)


def main() -> None:
    root = _repo_root()
    if root is None:
        _emit("graft: git yok (freshness atlandı)", {"available": False}, None)

    # Freshness from git: last commit that touched graft/, commits-behind, age.
    meta = _git(root, "log", "-1", "--format=%H|%cI", "--", "graft/")
    now = datetime.now(timezone.utc)
    if not meta or "|" not in meta:
        # No graft history at all → treat as needing a build.
        behind, age_h, last_commit = None, None, None
    else:
        last_commit, cdate = meta.split("|", 1)
        try:
            commit_dt = datetime.fromisoformat(cdate.strip())
            age_h = (now - commit_dt).total_seconds() / 3600.0
        except Exception:
            age_h = None
        cnt = _git(root, "rev-list", "--count", f"{last_commit}..HEAD")
        behind = int(cnt) if (cnt and cnt.isdigit()) else None

    logs = root / "logs"
    lock = logs / ".graft-refresh.lock"
    marker = logs / ".graft-auto-last-launch"

    def status(refreshing: bool) -> dict:
        return {
            "available": True,
            "behind": behind,
            "age_h": round(age_h, 1) if isinstance(age_h, float) else None,
            "last_commit": (last_commit[:12] if last_commit else None),
            "max_behind": MAX_BEHIND,
            "max_age_h": MAX_AGE_H,
            "refreshing": refreshing,
            "checked_at": now.isoformat(timespec="seconds"),
        }

    def fmt() -> str:
        b = "?" if behind is None else str(behind)
        a = "?" if age_h is None else f"{age_h:.0f}"
        return f"{b}c/{a}s"

    # A deep build already running? Report and do nothing.
    live = _lock_alive(lock)
    if live is not None:
        _emit(f"graft: --deep zaten koşuyor (pid {live})", status(True), root)

    # Double threshold (either alone is not enough), or no graft history yet.
    needs = (behind is None or age_h is None) or (behind > MAX_BEHIND and age_h > MAX_AGE_H)
    if not needs:
        _emit(f"graft: taze ({fmt()}, eşik altı)", status(False), root)

    # Stale — but was a launch fired very recently? Don't double-launch.
    try:
        if marker.exists() and (time.time() - marker.stat().st_mtime) < RELAUNCH_WINDOW_S:
            _emit(f"graft: bayat ({fmt()}) ama <30dk önce başlatıldı, atlanıyor",
                  status(True), root)
    except Exception:
        pass

    if DRY_RUN:
        _emit(f"graft: BAYAT ({fmt()}) → --deep başlatılırdı (dry-run, başlatılmadı)",
              status(False), root)

    # Launch the paid deep build, detached. The key stays inside graft-build.sh.
    try:
        logs.mkdir(parents=True, exist_ok=True)
        build = root / ".graft-kit" / "bin" / "graft-build.sh"
        log = logs / "graft-auto-refresh.log"
        with open(log, "a") as lf:
            lf.write(f"\n=== auto-refresh launch {now.isoformat(timespec='seconds')} "
                     f"({fmt()}, behind>{MAX_BEHIND} & age>{MAX_AGE_H}h) ===\n")
            lf.flush()
            proc = subprocess.Popen(
                ["bash", str(build), "--deep"],
                cwd=str(root), stdout=lf, stderr=lf,
                stdin=subprocess.DEVNULL, start_new_session=True,
                env={**os.environ, "LC_ALL": "C"},
            )
        lock.write_text(str(proc.pid))
        marker.touch()
        _emit(f"graft: BAYAT ({fmt()}) → arka planda --deep tazeleme başlatıldı "
              f"(pid {proc.pid}, ~dakikalar)", status(True), root)
    except Exception as exc:  # fail-open — never block the session
        try:
            (logs / "graft-auto-refresh.log").open("a").write(
                f"launch FAILED {now.isoformat(timespec='seconds')}: {exc}\n")
        except Exception:
            pass
        _emit(f"graft: bayat ({fmt()}) ama tazeleme başlatılamadı (fail-open)",
              status(False), root)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # Absolute backstop: never let this hook block a session.
        print("graft: auto-refresh hatası (fail-open)")
        sys.exit(0)
