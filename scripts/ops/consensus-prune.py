#!/usr/bin/env python3
"""consensus-prune.py — mechanical archive of old "What We Did This Cycle" entries.

Why (2026-10-08). The [PROMPT-SIZE] brake in auto-loop.sh fired on EVERY cycle from
2026-09-04 on: consensus.md had grown to 127 KB (82 KB of it 125 per-cycle entries), the
brake dropped it from the inline prompt and told the model to "prune stale material into
docs/" — a ritual no cycle ever performed. This script is that ritual as a harness
mechanism (loop-brake-design: intent != mechanism; fail-closed but never silent).

What it does, once per cycle, AFTER ledger-guard.py (whose rolling backup therefore
holds the pre-prune copy — the recovery source):
  1. Reads memories/consensus.md as bytes, strict UTF-8 (a decode error = skip, never
     errors="replace").
  2. Finds `## What We Did This Cycle` up to the next `^## ` line. Entries are top-level
     bullets `- **Cycle N` (separator after N is not part of the pattern) plus their
     continuation lines. Any other top-level bullet in the section = unknown shape = skip.
  3. Keeps the KEEP largest cycle NUMBERS (not positions); numbers must be strictly
     monotonic in file order, else skip.
  4. Appends the removed entries byte-exact to docs/operations/consensus-archive-YYYY-MM.md
     under a sha256-stamped header; a block whose sha is already in the archive is not
     appended again (idempotent). Archive is written and verified BEFORE consensus.
  5. Rewrites consensus atomically, leaving ONE "Archive note" line at the end of the
     section (older notes removed). The note deliberately avoids every word in
     ledger-guard's INCIDENT_RE so it cannot blind the content-loss alarm.
  6. Writes logs/consensus-prune.json {last_prune_cycle, pre_sha16, post_sha16, ...} —
     ledger-guard reads it to exempt exactly this one transition, nothing else.
  7. Counts consecutive skips while the file is over threshold; the 3rd prints an alarm
     line the harness forwards to Telegram. Fail-closed is not allowed to be quiet.

Triggers only when the file is >= CONSENSUS_PRUNE_MIN_BYTES (default 70000: the 120 KB
argv cap minus ~40 KB of non-consensus prompt minus a buffer) AND there is something to
archive. Env: CONSENSUS_PRUNE_ENABLED=0 (kill switch), CONSENSUS_PRUNE_KEEP (8; logs/runtime.env overrides the process env for every CONSENSUS_PRUNE_* key),
CONSENSUS_PRUNE_MIN_BYTES (70000), CONSENSUS_PRUNE_SKIP_ALARM (3).
Exit code is always 0 (informational helper; the loop never fails over it).
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

STATE_REL = "logs/consensus-prune.json"
CONSENSUS_REL = "memories/consensus.md"
ARCHIVE_DIR_REL = "docs/operations"
SECTION_HEADER = "## What We Did This Cycle"
ENTRY_RE = re.compile(r"^- \*\*Cycle\s+(\d+)")
TOP_BULLET_RE = re.compile(r"^- ")
# Prefix-only on purpose (2026-10-08, first prod week): the model wrote its own multi-line
# "- _Archive note (cycle 753): older ... entries for cycles 744-752 remain inline" and the
# strict `..._$` form refused the whole section for 24 cycles. Any line starting like an
# archive note — ours or the model's — is a note; its continuation lines are dropped with it
# and ONE fresh note is written back.
NOTE_RE = re.compile(r"^- _Archive note \(cycle \d+\):")
REQUIRED = ("# Auto Company Consensus", "## Next Action", "## Company State")
# Mirror of ledger-guard.INCIDENT_RE — the note must NOT match it (tested).
INCIDENT_WORDS_RE = re.compile(
    r"incident|restored|restore|inadvertent|geri getir|kay[ıi]p|lost|erased|truncat|overwr|reconstruct|prune|compacted",
    re.IGNORECASE,
)


_RUNTIME_ENV: dict = {}


def _load_runtime_env(app: Path) -> None:
    """logs/runtime.env is the operator's live override file (same idiom as
    IDLE_SKIP_ENABLED in auto-loop.sh): a key there beats the process env, so KEEP /
    MIN_BYTES / ENABLED can be tuned without a redeploy. Flat KEY=VALUE lines only."""
    try:
        for ln in (app / "logs/runtime.env").read_text(encoding="utf-8", errors="replace").splitlines():
            ln = ln.strip()
            if ln.startswith("CONSENSUS_PRUNE_") and "=" in ln:
                k, v = ln.split("=", 1)
                _RUNTIME_ENV[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass


def _env_int(name: str, default: int) -> int:
    try:
        v = int((_RUNTIME_ENV.get(name) or os.environ.get(name, "")).strip())
        return v if v > 0 else default
    except (ValueError, TypeError):
        return default


def _env_flag(name: str, default: str) -> str:
    return (_RUNTIME_ENV.get(name) or os.environ.get(name, default)).strip()


def _app(arg: str | None) -> Path:
    return Path(arg).resolve() if arg else Path(__file__).resolve().parents[2]


def _sha16(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


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


def _section_sizes(text: str) -> dict:
    parts = re.split(r"(?m)^(## .*)$", text)
    out = {}
    for i in range(1, len(parts), 2):
        out[parts[i].strip()] = len(parts[i + 1].encode("utf-8"))
    return out


class Skip(Exception):
    pass


def _split_section(lines: list[str]) -> tuple[int, int]:
    """Return (start, end) line indexes of the section body (exclusive end)."""
    start = None
    for i, ln in enumerate(lines):
        if ln.rstrip("\r\n") == SECTION_HEADER:
            start = i + 1
            break
    if start is None:
        raise Skip("section header not found")
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return start, end


def _parse_entries(body: list[str]) -> tuple[list[str], list[tuple[int, list[str]]], list[str]]:
    """Split section body into (preamble, entries[(cycle, lines)], tail-notes).

    Any top-level bullet that is not a Cycle entry or an Archive note = unknown shape → Skip.
    Lines before the first entry are preamble (kept). Archive-note lines are dropped (one
    fresh note is written back).
    """
    preamble: list[str] = []
    entries: list[tuple[int, list[str]]] = []
    cur: list[str] | None = None
    cur_n = None
    in_note = False  # dropping an old archive note and its continuation lines
    for ln in body:
        m = ENTRY_RE.match(ln)
        if m:
            if cur is not None:
                entries.append((cur_n, cur))
            cur_n, cur = int(m.group(1)), [ln]
            in_note = False
            continue
        if NOTE_RE.match(ln):
            if cur is not None:
                entries.append((cur_n, cur)); cur = None; cur_n = None
            in_note = True
            continue  # old note dropped; a single fresh one is re-added
        if TOP_BULLET_RE.match(ln):
            raise Skip(f"unrecognised top-level bullet: {ln.strip()[:60]!r}")
        if in_note:
            if ln.strip() == "":
                in_note = False  # blank line ends the note block
            continue
        if cur is None:
            preamble.append(ln)
        else:
            cur.append(ln)
    if cur is not None:
        entries.append((cur_n, cur))
    return preamble, entries, []


def _check_monotonic(entries: list[tuple[int, list[str]]]) -> None:
    nums = [n for n, _ in entries]
    if len(nums) != len(set(nums)):
        raise Skip("duplicate cycle numbers in section")
    desc = all(a > b for a, b in zip(nums, nums[1:]))
    asc = all(a < b for a, b in zip(nums, nums[1:]))
    if not (desc or asc):
        raise Skip("cycle numbers not monotonic")


def _archive_path(app: Path, now: _dt.datetime) -> Path:
    return app / ARCHIVE_DIR_REL / f"consensus-archive-{now:%Y-%m}.md"


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", type=int, required=True)
    ap.add_argument("--app", default=None)
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = ap.parse_args()

    app = _app(args.app)
    _load_runtime_env(app)
    if _env_flag("CONSENSUS_PRUNE_ENABLED", "1") == "0":
        return 0

    # KEEP default 8 (recalibrated after the first prod run, 2026-10-08: 12 entries = 29 KB
    # on top of 51 KB of non-entry sections left the prompt at 121.7 KB, 1.7 KB over the
    # cap). Still above work-window K=5 and turn-bloat K=3.
    keep = _env_int("CONSENSUS_PRUNE_KEEP", 8)
    min_bytes = _env_int("CONSENSUS_PRUNE_MIN_BYTES", 70000)
    skip_alarm = _env_int("CONSENSUS_PRUNE_SKIP_ALARM", 3)
    cpath = app / CONSENSUS_REL
    spath = app / STATE_REL
    state = _load_state(spath)
    streak = int(state.get("skipped_streak", 0) or 0)

    def finish_skip(reason: str, over: bool) -> int:
        nonlocal streak
        if over:
            streak += 1
        else:
            streak = 0
        if not args.dry_run:
            state["skipped_streak"] = streak
            state["last_cycle"] = args.cycle
            state["last_skip_reason"] = reason
            _save_state(spath, state)
        if over and streak >= skip_alarm:
            sys.stdout.write(
                f"⚠ CONSENSUS-PRUNE — Cycle #{args.cycle}: {streak} ardışık atlama ({reason}); "
                f"consensus.md eşik üstünde kalıyor, [PROMPT-SIZE] freni kapanmıyor. "
                f"Elle bak: scripts/ops/consensus-prune.py --dry-run.\n")
        elif over:
            sys.stdout.write(f"[CONSENSUS-PRUNE] skipped: {reason} (streak {streak})\n")
        return 0

    try:
        data = cpath.read_bytes()
    except Exception as e:
        return finish_skip(f"cannot read consensus: {e.__class__.__name__}", True)
    over = len(data) >= min_bytes
    if not over:
        if streak:
            state["skipped_streak"] = 0
            if not args.dry_run:
                _save_state(spath, state)
        return 0

    try:
        text = data.decode("utf-8")  # strict on purpose
    except UnicodeDecodeError:
        return finish_skip("consensus is not valid UTF-8", over)

    lines = text.splitlines(keepends=True)
    try:
        s, e = _split_section(lines)
        preamble, entries, _ = _parse_entries(lines[s:e])
        _check_monotonic(entries)
    except Skip as ex:
        return finish_skip(str(ex), over)

    sizes = _section_sizes(text)
    wwd_kb = sizes.get(SECTION_HEADER, 0) // 1024
    kd_kb = sizes.get("## Key Decisions Made", 0) // 1024
    if len(entries) <= keep:
        # Nothing left to archive yet the file is over threshold: that is not a prune
        # failure (no streak), it is the other sections outgrowing their share — the
        # trigger for a separate Key Decisions / section pass. Logged every cycle on purpose.
        if not args.dry_run:
            state["skipped_streak"] = 0
            state["last_cycle"] = args.cycle
            _save_state(spath, state)
        sys.stdout.write(f"[CONSENSUS-PRUNE] insufficient: {len(entries)} entries <= keep {keep}, file still "
                         f"{len(data)//1024}KB (whatwedid={wwd_kb}KB keydecisions={kd_kb}KB) — other sections need their own pass\n")
        return 0

    keep_nums = set(sorted((n for n, _ in entries), reverse=True)[:keep])
    kept = [(n, ls) for n, ls in entries if n in keep_nums]
    gone = [(n, ls) for n, ls in entries if n not in keep_nums]
    gone_nums = [n for n, _ in gone]
    lo, hi = min(gone_nums), max(gone_nums)
    block_text = "".join("".join(ls) for _, ls in gone)
    if not block_text.endswith("\n"):
        block_text += "\n"
    block_sha = hashlib.sha256(block_text.encode("utf-8")).hexdigest()
    now = _dt.datetime.now(_dt.timezone.utc)
    apath = _archive_path(app, now)
    arel = f"{ARCHIVE_DIR_REL}/{apath.name}"
    header = (f"\n## Archived at cycle {args.cycle} ({now:%Y-%m-%dT%H:%M:%SZ}) — "
              f"cycles {lo}..{hi} — {len(gone)} entries — sha256:{block_sha}\n\n")
    note = (f"- _Archive note (cycle {args.cycle}): {len(gone)} older entries (cycles {lo}..{hi}) "
            f"moved to {arel}. Not for routine reading — grep by cycle number only._\n")
    assert not INCIDENT_WORDS_RE.search(note), "archive note must not match INCIDENT_RE"

    new_body = preamble + [l for _, ls in kept for l in ls]
    if new_body and not new_body[-1].endswith("\n"):
        new_body[-1] += "\n"
    if new_body and new_body[-1].strip() != "":
        new_body.append("\n")
    new_body.append(note)
    new_body.append("\n")
    new_lines = lines[:s] + new_body + lines[e:]
    new_text = "".join(new_lines)
    for req in REQUIRED:
        if req not in new_text:
            return finish_skip(f"result would lose required marker {req!r}", over)
    new_data = new_text.encode("utf-8")

    summary = (f"[CONSENSUS-PRUNE] cycle {args.cycle}: {len(gone)} entries (cycles {lo}..{hi}) moved to "
               f"{arel}; kept {len(kept)}; {len(data)//1024}KB -> {len(new_data)//1024}KB "
               f"(whatwedid={wwd_kb}KB keydecisions={kd_kb}KB)")
    if len(new_data) > 80000:
        summary += " insufficient: still >80KB after archive — Key Decisions/other sections need their own pass"
    if args.dry_run:
        sys.stdout.write(summary + " [dry-run]\n")
        return 0

    # 1) archive first, verified, idempotent
    try:
        apath.parent.mkdir(parents=True, exist_ok=True)
        existing = apath.read_bytes() if apath.is_file() else b""
        if f"sha256:{block_sha}".encode() not in existing:
            with open(apath, "ab") as fh:
                fh.write(header.encode("utf-8") + block_text.encode("utf-8"))
                fh.flush(); os.fsync(fh.fileno())
        if f"sha256:{block_sha}".encode() not in apath.read_bytes():
            return finish_skip("archive verification failed", over)
    except Exception as ex:
        return finish_skip(f"archive write failed: {ex.__class__.__name__}", over)

    # 2) consensus, atomically, only if nobody wrote it meanwhile
    try:
        if cpath.read_bytes() != data:
            return finish_skip("consensus changed during run", over)
        tmp = cpath.with_name(cpath.name + ".prune-tmp")
        tmp.write_bytes(new_data)
        os.replace(tmp, cpath)
    except Exception as ex:
        return finish_skip(f"consensus write failed: {ex.__class__.__name__}", over)

    # post_metrics mirrors ledger-guard._metrics so the guard can rebase its baseline.
    post_metrics = {
        "sections": len(re.findall(r"(?m)^## ", new_text)),
        "rows": len(set(re.findall(r"OPEX Kalemleri!A\d+", new_text))),
        "bytes": len(new_data),
        "sha16": _sha16(new_data),
        "incident": bool(INCIDENT_WORDS_RE.search(new_text)),
    }
    state.update({
        "last_prune_cycle": args.cycle,
        "pre_sha16": _sha16(data),
        "post_sha16": _sha16(new_data),
        "post_metrics": post_metrics,
        "bytes_before": len(data),
        "bytes_after": len(new_data),
        "archive": arel,
        "block_sha256": block_sha,
        "skipped_streak": 0,
        "last_cycle": args.cycle,
    })
    _save_state(spath, state)
    sys.stdout.write(summary + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # informational: never fail the loop
