#!/usr/bin/env python3
"""work-window-watchdog.py — the ALARM layer paired with the work-window brake.

The brake (work-window.py) injects an order forbidding an empty-cycle confirmation while
a work-window is open. A model can still ignore an injected order (the very reason the
brake exists — a rule the model may skip is not a mechanism). This watchdog makes that
failure VISIBLE instead of silent: if the window was open AND the model emitted an
empty-cycle admission for THRESHOLD consecutive cycles, it prints one Telegram alarm.

It is an ALARM, not a brake: it never blocks or reruns a cycle, and it cannot perfectly
tell a lazy empty cycle from a correctly-reported "everything is blocked" cycle. It says
"look here", and a human (or the external watcher) judges. THRESHOLD=2 consecutive avoids
firing on a single stray empty, and it emits once on crossing (not every cycle) to stay
quiet.

Contract with the harness:
  stdin  : this cycle's model output (RESULT_TEXT + the consensus "What We Did" head)
  args   : --cycle N --app PATH --open 0|1 (was the window open) --failed 0|1 (cycle failed)
  stdout : a one-line alarm if the threshold was just crossed, else empty
  exit   : always 0 (informational; never fails the loop)

State: logs/work-window-watchdog.json {consecutive, last_cycle}. A window-closed cycle, a
failed cycle, or a cycle with real work resets the counter to 0.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

STATE_REL = "logs/work-window-watchdog.json"
DEFAULT_THRESHOLD = 2
# The lazy-idle phrasings the model uses when it skips work. Deliberately NOT generic
# words like "blocked"/"sponsor" — the brake's escape clause tells the model to ENUMERATE
# blocked items instead of writing a bare empty-cycle line, so those produce different text.
EMPTY_RE = re.compile(
    r"empty[\s-]*cycle|correct empty|no permitted work|recorded as an empty|no state (?:changed|moved)",
    re.IGNORECASE,
)


def _app_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg).resolve()
    return Path(__file__).resolve().parents[2]


def _threshold() -> int:
    raw = os.environ.get("WORK_WINDOW_WATCHDOG_THRESHOLD", "").strip()
    try:
        v = int(raw)
        return v if v >= 1 else DEFAULT_THRESHOLD
    except ValueError:
        return DEFAULT_THRESHOLD


def _read_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_state(path: Path, state: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, path)
    except Exception:
        pass  # never fail the loop over a bookkeeping write


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", type=int, required=True)
    ap.add_argument("--app", default=None)
    ap.add_argument("--open", dest="open_", default="0")
    ap.add_argument("--failed", default="0")
    args = ap.parse_args()

    app = _app_dir(args.app)
    state_path = app / STATE_REL
    state = _read_state(state_path)
    consecutive = int(state.get("consecutive", 0) or 0)
    threshold = _threshold()

    window_open = str(args.open_).strip() == "1"
    cycle_failed = str(args.failed).strip() == "1"

    # Reset conditions: window was closed (normal idle is fine), or the cycle failed
    # (a timeout/crash is not an empty-cycle violation).
    if not window_open or cycle_failed:
        if consecutive != 0:
            _write_state(state_path, {"consecutive": 0, "last_cycle": args.cycle})
        return 0

    try:
        text = sys.stdin.read()
    except Exception:
        text = ""

    if not EMPTY_RE.search(text or ""):
        # Real work happened in an open window -> reset.
        if consecutive != 0:
            _write_state(state_path, {"consecutive": 0, "last_cycle": args.cycle})
        return 0

    # Violation: window open but the model emitted an empty-cycle admission.
    consecutive += 1
    _write_state(state_path, {"consecutive": consecutive, "last_cycle": args.cycle})

    # Emit exactly once, on crossing the threshold, to stay quiet if it persists.
    if consecutive == threshold:
        sys.stdout.write(
            f"⚠ WORK-WINDOW WATCHDOG — Cycle #{args.cycle}: the work-window brake was OPEN "
            f"but the loop emitted an empty-cycle confirmation {consecutive} cycles in a row. "
            f"Either the follow-on work is genuinely all blocked-by-authority (then it should "
            f"be enumerated, not skipped), or the brake is being ignored. Check "
            f"memories/consensus.md Next Action + the conflict ledger.\n"
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        # Informational tool: any error is swallowed so it can never fail the loop.
        sys.exit(0)
