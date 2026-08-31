#!/usr/bin/env python3
"""turn-bloat-brake.py — escalate on a STREAK of BLOATED cycles.

The turn-audit already flags a single BLOATED cycle (turns>65 / dur>=675s / cost>=$5) and
injects an advisory `_turnfb_line` into the next cycle. That advisory is per-cycle and easy
to ignore — the Program Audit found 4 BLOATED cycles in a day that also damaged the ledger.
This brake tracks CONSECUTIVE BLOATED cycles and, once a streak reaches K (default 3):
  * --record : prints ONE Telegram alarm on the crossing (harness pipes it to telegram-notify),
  * --feedback : prints a HARD mandate line the harness injects in place of the soft advisory.

Any non-BLOATED verdict resets the streak. Informational: exits 0 always, never fails the loop.
Kill switch TURN_BLOAT_ENABLED=0. Streak length TURN_BLOAT_STREAK (default 3).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

STATE_REL = "logs/turn-bloat-state.json"


def _app(arg: str | None) -> Path:
    return Path(arg).resolve() if arg else Path(__file__).resolve().parents[2]


def _streak_len() -> int:
    try:
        v = int(os.environ.get("TURN_BLOAT_STREAK", "").strip())
        return v if v >= 1 else 3
    except (ValueError, TypeError):
        return 3


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save(path: Path, st: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, path)
    except Exception:
        pass


HARD_LINE = (
    "⛔ TURN-ECONOMY HARD BRAKE — {n} cycles BLOATED in a row. This cycle you MUST: pick "
    "exactly ONE bounded milestone, persist it to memories/consensus.md, and END — do NOT keep "
    "investigating or appending. Long append-heavy cycles have damaged the ledger (Program Audit "
    "2026-08-31, §3.1). If the state snapshot's DELTA is none, the correct output is a single "
    "short line, not more exploration."
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--feedback", action="store_true")
    ap.add_argument("--cycle", type=int, default=0)
    ap.add_argument("--verdict", default="")
    ap.add_argument("--app", default=None)
    args = ap.parse_args()

    if os.environ.get("TURN_BLOAT_ENABLED", "1").strip() == "0":
        return 0

    app = _app(args.app)
    state_path = app / STATE_REL
    st = _load(state_path)
    consecutive = int(st.get("consecutive", 0) or 0)
    k = _streak_len()

    if args.feedback:
        # Pre-cycle: emit the hard mandate only while a streak is active.
        if consecutive >= k:
            sys.stdout.write(HARD_LINE.format(n=consecutive) + "\n")
        return 0

    if args.record:
        v = (args.verdict or "").strip().upper()
        if v == "BLOATED":
            consecutive += 1
        else:
            consecutive = 0
        _save(state_path, {"consecutive": consecutive, "last_cycle": args.cycle})
        # Alarm exactly on the crossing, then stay quiet so a long streak is not spammy.
        if consecutive == k:
            sys.stdout.write(
                f"⛔ TURN-BLOAT — {consecutive} cycles BLOATED in a row (turns>65). "
                f"Long append-heavy cycles are the pattern that damaged the ledger (Program Audit "
                f"§3.1). The loop has been given a hard persist-and-end mandate; check "
                f"memories/cost-audit.md and consensus.md.\n"
            )
        return 0

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
