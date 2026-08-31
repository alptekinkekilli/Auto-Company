#!/usr/bin/env python3
"""Tests for scripts/ops/ledger-guard.py. Run: python3 tests/test_ledger_guard.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "ops" / "ledger-guard.py"
_fail = []


def newapp():
    d = Path(tempfile.mkdtemp())
    (d / "docs/operations").mkdir(parents=True)
    (d / "memories").mkdir(parents=True)
    (d / "logs").mkdir(parents=True)
    return d


def ledger(d):
    return d / "docs/operations/wowcar-gate0-source-of-truth-and-conflict-ledger-test.md"


def run(d, cycle, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([sys.executable, str(SCRIPT), "--cycle", str(cycle), "--app", str(d)],
                       capture_output=True, text=True, env=e)
    return p.returncode, p.stdout


def body(sections, rows, extra=""):
    s = "# Ledger\n\n"
    for i in range(sections):
        s += f"## {i+1}. section {i}\nbody line\n\n"
    for r in rows:
        s += f"OPEX Kalemleri!A{r}:D{r} row {r}\n"
    return s + extra


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        _fail.append(name)


# Always exits 0.
d = newapp()
ledger(d).write_text(body(10, range(6, 20)), encoding="utf-8")
rc, out = run(d, 100)
check("first run exits 0", rc == 0)
check("first run: no alarm (no prev)", "LEDGER-GUARD" not in out)
check("first run: backup created", any((d / "logs/state-backups").glob("100-*")))
check("first run: state written", (d / "logs/ledger-guard.json").is_file())

# Unchanged -> silent.
rc, out = run(d, 101)
check("unchanged: silent", out.strip() == "")

# Section drop >=2 -> alarm.
ledger(d).write_text(body(7, range(6, 20)), encoding="utf-8")  # 10 -> 7 sections
rc, out = run(d, 102)
check("section drop => alarm", "LEDGER-GUARD" in out and "sections" in out)

# Row drop -> alarm (drop 3 rows).
d = newapp(); ledger(d).write_text(body(10, range(6, 20)), encoding="utf-8"); run(d, 1)
ledger(d).write_text(body(10, range(6, 17)), encoding="utf-8")  # 14 -> 11 rows
rc, out = run(d, 2)
check("row drop => alarm", "LEDGER-GUARD" in out and "OPEX rows" in out)

# Size drop >=15% -> alarm.
d = newapp(); ledger(d).write_text(body(10, range(6, 20)) + "X" * 5000, encoding="utf-8"); run(d, 1)
ledger(d).write_text(body(10, range(6, 20)), encoding="utf-8")  # lost ~5000 bytes
rc, out = run(d, 2)
check("size drop => alarm", "LEDGER-GUARD" in out and "size" in out)

# Incident-note exemption: same drop but with an incident marker -> silent.
d = newapp(); ledger(d).write_text(body(10, range(6, 20)), encoding="utf-8"); run(d, 1)
ledger(d).write_text(body(7, range(6, 20), extra="\nincident: sections pruned into docs/, reconstructable\n"), encoding="utf-8")
rc, out = run(d, 2)
check("incident-note drop => silent", "LEDGER-GUARD" not in out)

# File missing after being present -> alarm.
d = newapp(); ledger(d).write_text(body(10, range(6, 20)), encoding="utf-8"); run(d, 1)
ledger(d).unlink()
rc, out = run(d, 2)
check("file missing => alarm", "LEDGER-GUARD" in out and "MISSING" in out)

# Backup rotation: keep=3.
d = newapp(); ledger(d).write_text(body(10, range(6, 20)), encoding="utf-8")
for c in range(1, 7):
    ledger(d).write_text(body(10, range(6, 20)) + f"\ncycle{c}\n", encoding="utf-8")
    run(d, c, env={"LEDGER_GUARD_KEEP": "3"})
bks = list((d / "logs/state-backups").glob("*-wowcar-gate0-source-of-truth-and-conflict-ledger-test.md"))
check("backup rotation keeps 3", len(bks) == 3)

# Kill switch.
d = newapp(); ledger(d).write_text(body(10, range(6, 20)), encoding="utf-8"); run(d, 1)
ledger(d).write_text(body(3, range(6, 8)), encoding="utf-8")  # huge drop
rc, out = run(d, 2, env={"LEDGER_GUARD_ENABLED": "0"})
check("kill switch: silent + no backup this run", out.strip() == "" and not any((d / "logs/state-backups").glob("2-*")))

print()
if _fail:
    print(f"{len(_fail)} FAILURE(S): " + ", ".join(_fail)); sys.exit(1)
print("ALL TESTS PASSED")
