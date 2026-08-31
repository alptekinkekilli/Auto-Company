#!/usr/bin/env python3
"""Tests for scripts/ops/turn-bloat-brake.py. Run: python3 tests/test_turn_bloat_brake.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "ops" / "turn-bloat-brake.py"
_fail = []


def newapp():
    d = Path(tempfile.mkdtemp())
    (d / "logs").mkdir(parents=True)
    return d


def rec(d, cycle, verdict, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([sys.executable, str(SCRIPT), "--record", "--cycle", str(cycle),
                        "--verdict", verdict, "--app", str(d)], capture_output=True, text=True, env=e)
    return p.returncode, p.stdout


def fb(d, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([sys.executable, str(SCRIPT), "--feedback", "--app", str(d)],
                       capture_output=True, text=True, env=e)
    return p.stdout


def consecutive(d):
    return json.loads((d / "logs/turn-bloat-state.json").read_text()).get("consecutive")


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        _fail.append(name)


# Single BLOATED: consecutive=1, no alarm (< K=3), no hard feedback.
d = newapp()
rc, out = rec(d, 1, "BLOATED")
check("1 bloated: exit 0", rc == 0)
check("1 bloated: consecutive=1", consecutive(d) == 1)
check("1 bloated: no alarm", out.strip() == "")
check("1 bloated: no hard feedback", fb(d).strip() == "")

# 2nd BLOATED: consecutive=2, still no alarm.
rec(d, 2, "BLOATED")
check("2 bloated: consecutive=2", consecutive(d) == 2)
check("2 bloated: no hard feedback yet", fb(d).strip() == "")

# 3rd consecutive BLOATED: crossing K -> alarm + hard feedback active.
rc, out = rec(d, 3, "BLOATED")
check("3 bloated: alarm fires on crossing", "TURN-BLOAT" in out)
check("3 bloated: consecutive=3", consecutive(d) == 3)
check("3 bloated: hard feedback active", "HARD BRAKE" in fb(d))

# 4th BLOATED: past crossing -> stays quiet (no repeat alarm), feedback still active.
rc, out = rec(d, 4, "BLOATED")
check("4 bloated: no repeat alarm", out.strip() == "")
check("4 bloated: feedback still active", "HARD BRAKE" in fb(d))

# ok verdict resets the streak.
rec(d, 5, "ok")
check("ok resets consecutive to 0", consecutive(d) == 0)
check("ok clears hard feedback", fb(d).strip() == "")

# CHATTY also resets (only BLOATED counts).
rec(d, 6, "BLOATED"); rec(d, 7, "CHATTY")
check("chatty resets streak", consecutive(d) == 0)

# Env streak length K=2.
d = newapp()
rec(d, 1, "BLOATED", env={"TURN_BLOAT_STREAK": "2"})
rc, out = rec(d, 2, "BLOATED", env={"TURN_BLOAT_STREAK": "2"})
check("env K=2: alarm on 2nd", "TURN-BLOAT" in out)
check("env K=2: hard feedback active", "HARD BRAKE" in fb(d, env={"TURN_BLOAT_STREAK": "2"}))

# Kill switch.
d = newapp()
rc, out = rec(d, 1, "BLOATED", env={"TURN_BLOAT_ENABLED": "0"})
check("kill switch: no state written", not (d / "logs/turn-bloat-state.json").is_file())

print()
if _fail:
    print(f"{len(_fail)} FAILURE(S): " + ", ".join(_fail)); sys.exit(1)
print("ALL TESTS PASSED")
