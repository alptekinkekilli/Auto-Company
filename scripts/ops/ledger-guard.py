#!/usr/bin/env python3
"""ledger-guard.py — per-cycle integrity guard + recovery source for the Gate-0
conflict ledger and consensus.md.

Program Audit 2026-08-31 found the Gate-0 ledger silently LOST content (whole §5*/§6
sections, the exit criteria, and 3 OPEX-row classification records) across bloated
append-heavy cycles, with no incident note and no cycle noticing — and the ledger has
NO harness protection and is NOT in git (docs/operations is gitignored), so there was
no backup and no version trail to recover from.

This guard, run post-cycle, does two things per guarded file:
  1. ROLLING BACKUP -> logs/state-backups/<cycle>-<basename> (keep last N) — the recovery
     source that did not exist before.
  2. LOSS DETECTION vs the previous cycle's metrics (logs/ledger-guard.json): section-header
     count (^## ), row-ref count (OPEX Kalemleri!A<n>), byte size, sha16. If a metric DROPS
     beyond threshold AND the new content carries no incident marker, print a VIOLATION line
     (the harness pipes it to Telegram) — silent content loss becomes visible.

Informational: exits 0 ALWAYS (never fails the loop). A backup write error or an unreadable
file is swallowed. Thresholds/retention are env-overridable. Kill switch LEDGER_GUARD_ENABLED=0.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

STATE_REL = "logs/ledger-guard.json"
BACKUP_DIR_REL = "logs/state-backups"
SECTION_RE = re.compile(r"^## ", re.MULTILINE)
ROWREF_RE = re.compile(r"OPEX Kalemleri!A\d+")
INCIDENT_RE = re.compile(
    r"incident|restored|restore|inadvertent|geri getir|kay[ıi]p|lost|erased|truncat|overwr|reconstruct",
    re.IGNORECASE,
)


def _env_int(name: str, default: int) -> int:
    try:
        v = int(os.environ.get(name, "").strip())
        return v if v > 0 else default
    except (ValueError, TypeError):
        return default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, "").strip())
    except (ValueError, TypeError):
        return default


def _app(arg: str | None) -> Path:
    return Path(arg).resolve() if arg else Path(__file__).resolve().parents[2]


def _find_ledger(app: Path) -> Path | None:
    """The live Gate-0 conflict ledger (most-recently-modified match)."""
    cands = glob.glob(str(app / "docs/operations/*gate0*conflict-ledger*.md"))
    if not cands:
        cands = glob.glob(str(app / "docs/operations/*conflict-ledger*.md"))
    if not cands:
        return None
    return Path(max(cands, key=lambda p: os.path.getmtime(p)))


def _metrics(path: Path) -> dict | None:
    try:
        data = path.read_bytes()
    except Exception:
        return None
    text = data.decode("utf-8", errors="replace")
    return {
        "sections": len(SECTION_RE.findall(text)),
        "rows": len(set(ROWREF_RE.findall(text))),
        "bytes": len(data),
        "sha16": hashlib.sha256(data).hexdigest()[:16],
        "incident": bool(INCIDENT_RE.search(text)),
    }


def _backup(app: Path, cycle: int, path: Path, keep: int) -> None:
    try:
        bdir = app / BACKUP_DIR_REL
        bdir.mkdir(parents=True, exist_ok=True)
        dest = bdir / f"{cycle}-{path.name}"
        shutil.copy2(path, dest)
        # rotate: keep newest `keep` backups per basename
        same = sorted(bdir.glob(f"*-{path.name}"), key=lambda p: p.stat().st_mtime, reverse=True)
        for old in same[keep:]:
            try:
                old.unlink()
            except Exception:
                pass
    except Exception:
        pass  # never fail the loop over a backup


def _load_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_state(path: Path, state: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, path)
    except Exception:
        pass


def _check(name: str, cur: dict | None, prev: dict | None,
           drop_sections: int, drop_rows: int, drop_frac: float) -> str | None:
    """Return a violation string if cur lost content vs prev without an incident marker."""
    if prev is None:
        return None  # first observation of this file
    if cur is None:
        # File was present before and is now unreadable/gone — major loss.
        return (f"{name}: file MISSING or unreadable (previously {prev.get('sections','?')} "
                f"sections / {prev.get('bytes','?')} bytes). Investigate immediately.")
    if cur.get("sha16") == prev.get("sha16"):
        return None  # unchanged
    if cur.get("incident"):
        return None  # the cycle documented a repair/incident — expected churn
    reasons = []
    ds = prev["sections"] - cur["sections"]
    dr = prev["rows"] - cur["rows"]
    db = prev["bytes"] - cur["bytes"]
    if ds >= drop_sections:
        reasons.append(f"sections {prev['sections']}→{cur['sections']} (−{ds})")
    if dr >= drop_rows:
        reasons.append(f"OPEX rows {prev['rows']}→{cur['rows']} (−{dr})")
    if prev["bytes"] > 0 and db > 0 and (db / prev["bytes"]) >= drop_frac:
        reasons.append(f"size {prev['bytes']}→{cur['bytes']} (−{db}B, {100*db/prev['bytes']:.0f}%)")
    if not reasons:
        return None
    return f"{name}: content dropped without an incident note — " + "; ".join(reasons)


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", type=int, required=True)
    ap.add_argument("--app", default=None)
    args = ap.parse_args()

    if os.environ.get("LEDGER_GUARD_ENABLED", "1").strip() == "0":
        return 0

    app = _app(args.app)
    keep = _env_int("LEDGER_GUARD_KEEP", 15)
    drop_sections = _env_int("LEDGER_GUARD_DROP_SECTIONS", 2)
    drop_rows = _env_int("LEDGER_GUARD_DROP_ROWS", 1)
    drop_frac = _env_float("LEDGER_GUARD_DROP_FRAC", 0.15)

    guarded: list[tuple[str, Path]] = []
    ledger = _find_ledger(app)
    if ledger is not None:
        guarded.append(("ledger", ledger))
    consensus = app / "memories/consensus.md"
    if consensus.is_file():
        guarded.append(("consensus", consensus))

    state_path = app / STATE_REL
    state = _load_state(state_path)
    prev_metrics = state.get("metrics", {})
    new_metrics = {}
    violations = []

    seen = set()
    for name, path in guarded:
        seen.add(name)
        _backup(app, args.cycle, path, keep)
        cur = _metrics(path)
        v = _check(name, cur, prev_metrics.get(name), drop_sections, drop_rows, drop_frac)
        if v:
            violations.append(v)
        if cur is not None:
            new_metrics[name] = cur
        elif prev_metrics.get(name):
            new_metrics[name] = prev_metrics[name]  # keep last-known so we keep alarming

    # A file tracked last cycle that we can no longer even locate is a MAJOR loss.
    for name, prev in prev_metrics.items():
        if name in seen:
            continue
        v = _check(name, None, prev, drop_sections, drop_rows, drop_frac)
        if v:
            violations.append(v)
        new_metrics[name] = prev  # keep last-known so we keep alarming until restored

    state["metrics"] = new_metrics
    state["last_cycle"] = args.cycle
    _save_state(state_path, state)

    if violations:
        sys.stdout.write(
            f"⚠ LEDGER-GUARD — Cycle #{args.cycle}: state-file content loss detected.\n"
            + "\n".join(f"  • {v}" for v in violations)
            + f"\n  Recovery: logs/state-backups/ holds the last {keep} cycles' copies. "
            + "The controlling Gate-0 ledger may now overstate its evidence (directive §16).\n"
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # informational: never fail the loop
