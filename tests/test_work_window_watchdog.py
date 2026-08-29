#!/usr/bin/env python3
"""Tests for scripts/ops/work-window-watchdog.py — the work-window alarm layer.

Run: python3 tests/test_work_window_watchdog.py
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "ops" / "work-window-watchdog.py"
_failures = []


def run(text, cycle, *, open_="1", failed="0", app=None, env=None):
    tmp = app or tempfile.mkdtemp()
    (Path(tmp) / "logs").mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(SCRIPT), "--cycle", str(cycle), "--app", str(tmp),
           "--open", open_, "--failed", failed]
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(cmd, input=text, capture_output=True, text=True, env=e)
    sp = Path(tmp) / "logs" / "work-window-watchdog.json"
    st = json.loads(sp.read_text()) if sp.is_file() else None
    return p.returncode, p.stdout, st, tmp


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        _failures.append(name)


# Never fails the loop: always exit 0.
rc, out, st, tmp = run("Cycle did real work: closed C13.", 100)
check("real work exits 0", rc == 0)
check("real work no alarm", out.strip() == "")
check("real work resets/keeps consecutive 0", (st or {}).get("consecutive", 0) == 0)

# Window closed -> reset, no alarm even with empty text.
rc, out, st, tmp = run("EMPTY CYCLE", 101, open_="0")
check("window closed => exit 0, no alarm", rc == 0 and out.strip() == "")

# Failed cycle -> not a violation.
rc, out, st, tmp = run("EMPTY CYCLE", 102, failed="1")
check("failed cycle => no alarm", out.strip() == "")

# One empty-while-open (consecutive=1 < threshold 2) -> no alarm yet, state records 1.
tmp = tempfile.mkdtemp()
rc, out, st, _ = run("Cycle #103: EMPTY CYCLE (correct per standing mode).", 103, app=tmp)
check("first violation: no alarm", out.strip() == "")
check("first violation: consecutive=1", st and st.get("consecutive") == 1)

# Second consecutive empty-while-open -> alarm fires (threshold 2), consecutive=2.
rc, out, st, _ = run("Cycle #104: empty cycle, no state changed.", 104, app=tmp)
check("second violation: alarm fires", "WORK-WINDOW WATCHDOG" in out)
check("second violation: consecutive=2", st and st.get("consecutive") == 2)

# Third consecutive -> stays quiet (emit only on crossing), consecutive=3.
rc, out, st, _ = run("Cycle #105: recorded as an empty cycle.", 105, app=tmp)
check("third violation: quiet (emit once on crossing)", out.strip() == "")
check("third violation: consecutive=3", st and st.get("consecutive") == 3)

# Real work after violations -> reset to 0.
rc, out, st, _ = run("Closed conflict C09 with cell evidence.", 106, app=tmp)
check("real work resets consecutive to 0", st and st.get("consecutive") == 0)

# Escape clause must NOT false-positive: enumerated blockers, no bare empty phrasing.
rc, out, st, tmp2 = run("Remaining items are all blocked-by-authority: C14 sponsor, C15 counsel. Advanced nothing.", 107)
check("blocked-enumeration (no empty phrase) => no alarm", out.strip() == "")

# Threshold via env (=1 -> alarm on first violation).
tmp3 = tempfile.mkdtemp()
rc, out, st, _ = run("EMPTY CYCLE.", 108, app=tmp3, env={"WORK_WINDOW_WATCHDOG_THRESHOLD": "1"})
check("env threshold=1 alarms on first violation", "WORK-WINDOW WATCHDOG" in out)

print()
if _failures:
    print(f"{len(_failures)} FAILURE(S): " + ", ".join(_failures))
    sys.exit(1)
print("ALL TESTS PASSED")
