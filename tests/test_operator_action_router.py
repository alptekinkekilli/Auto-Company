#!/usr/bin/env python3
"""Tests for scripts/ops/operator-action-router.py — the operator-action digest watcher.

  python3 tests/test_operator_action_router.py

Exercises the REAL functions (collect_items / render / should_notify) and a real main()
run with notify() monkeypatched to a recorder, so state persistence and dedup are tested on
the true code path — not a re-implementation.
"""
import importlib.util
import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "scripts", "ops", "operator-action-router.py")

spec = importlib.util.spec_from_file_location("oar", SRC)
oar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oar)

fail = 0


def check(name, got, want):
    global fail
    if got == want:
        print(f"  PASS {name}")
    else:
        print(f"  FAIL {name}: expected {want!r} got {got!r}")
        fail = 1


def check_true(name, cond):
    check(name, bool(cond), True)


def make_app(hold=None, opreqs=None, directive=None, directive_age_h=None):
    """Build a throwaway --app tree. directive=(status); age set via mtime."""
    d = tempfile.mkdtemp(prefix="oar-")
    os.makedirs(os.path.join(d, "logs"))
    os.makedirs(os.path.join(d, "memories"))
    # a stub telegram-notify.sh so notify() has a script to find (monkeypatched anyway)
    os.makedirs(os.path.join(d, "scripts", "core"))
    with open(os.path.join(d, "scripts", "core", "telegram-notify.sh"), "w") as fh:
        fh.write("#!/usr/bin/env bash\ncat >/dev/null\n")

    if hold is not None:
        with open(os.path.join(d, "logs", "LOOP_HOLD"), "w") as fh:
            fh.write(f"latched 2026-08-26T00:00:00Z\nreason {hold}\n"
                     "cleared_by operator only\n")
    if opreqs:
        blocks = []
        for rid, status in opreqs:
            blocks.append(f"## {rid}\n- Type: legal\n- Status: {status}\n- Blocked scope: x\n")
        with open(os.path.join(d, "memories", "operator-requests.md"), "w") as fh:
            fh.write("<!-- ledger -->\n\n" + "\n".join(blocks))
    if directive is not None:
        p = os.path.join(d, "memories", "human-directive.md")
        with open(p, "w") as fh:
            fh.write(f"# Directive\n\n## Status\n{directive}\n\n## Directive\nbody\n")
        if directive_age_h is not None:
            old = time.time() - directive_age_h * 3600
            os.utime(p, (old, old))
    return d


# --- 1: full set → digest lists all three, in priority order, with resolution paths ---
print("--- 1: all three blockers present ---")
app = make_app(hold="budget spend unparseable",
               opreqs=[("OPREQ-OPEX-14", "OPEN"), ("OPREQ-OPEX-15", "OPEN")],
               directive="PENDING", directive_age_h=50)
items = oar.collect_items(app, directive_min_hours=12)
check("three items", len(items), 3)
check("priority order = hold,opreq,directive",
      [it["priority"] for it in items], [oar.P_HOLD, oar.P_OPREQ, oar.P_DIRECTIVE])
digest = oar.render(items)
check("header counts 3", digest.splitlines()[0], "🧭 Sende 3 açık iş:")
check_true("hold line + resolution", "[HOLD]" in digest and "/release" in digest)
check_true("opreq ids + resolution",
           "OPREQ-OPEX-14" in digest and "OPREQ-OPEX-15" in digest and "karar kartı" in digest)
check_true("directive age + resolution", "[DIRECTIVE] PENDING 50s" in digest and "directive slot" in digest)
check_true("footer", digest.strip().endswith("Gerisi normal."))

# --- 2: empty set → silent, no notify, state cleared ---
print("--- 2: nothing open → silent ---")
app2 = make_app(directive="DONE")  # DONE is not PENDING → no item
items2 = oar.collect_items(app2, directive_min_hours=12)
check("no items", items2, [])
sent = []
oar.notify = lambda a, t: sent.append(t)  # monkeypatch
sys.argv = ["oar", "--app", app2]
rc = oar.main()
check("main returns 0 on empty", rc, 0)
check("nothing sent on empty", sent, [])

# --- 3: fresh PENDING directive below floor is NOT an item (matches staleness floor) ---
print("--- 3: directive PENDING but younger than floor ---")
app3 = make_app(directive="PENDING", directive_age_h=2)
check("young pending skipped", oar.collect_items(app3, directive_min_hours=12), [])
check_true("old pending included",
           len(oar.collect_items(app3, directive_min_hours=1)) == 1)

# --- 4: dedup — same open set within repeat window notifies once ---
print("--- 4: dedup across two real runs ---")
app4 = make_app(opreqs=[("OPREQ-A", "OPEN")])
sent4 = []
oar.notify = lambda a, t: sent4.append(t)
sys.argv = ["oar", "--app", app4, "--repeat-hours", "24"]
oar.main()
oar.main()  # identical set, within window
check("notified exactly once (dedup)", len(sent4), 1)
state = json.load(open(os.path.join(app4, oar.STATE_REL)))
check_true("state has hash + timestamp", "hash" in state and "last_notified_iso" in state)

# --- 4b: the set CHANGING re-notifies even within the window ---
print("--- 4b: changed set breaks dedup ---")
with open(os.path.join(app4, "memories", "operator-requests.md"), "a") as fh:
    fh.write("\n## OPREQ-B\n- Status: OPEN\n")
oar.main()
check("re-notified on changed set", len(sent4), 2)

# --- 5: empty set clears prior state so the next open item alerts immediately ---
print("--- 5: empty clears persisted state ---")
app5 = make_app(opreqs=[("OPREQ-Z", "OPEN")])
sent5 = []
oar.notify = lambda a, t: sent5.append(t)
sys.argv = ["oar", "--app", app5]
oar.main()
check_true("state written", os.path.exists(os.path.join(app5, oar.STATE_REL)))
# resolve it → set becomes empty
with open(os.path.join(app5, "memories", "operator-requests.md"), "w") as fh:
    fh.write("## OPREQ-Z\n- Status: RESOLVED\n")
oar.main()
check("state cleared on empty", os.path.exists(os.path.join(app5, oar.STATE_REL)), False)

# --- 6: fail-soft — missing memories/ dir must not crash, other sources still reported ---
print("--- 6: fail-soft on unreadable source ---")
app6 = make_app(hold="latch reason")  # no memories/*.md files at all besides dir
# remove the whole memories dir to force OSError on both opreq + directive reads
import shutil
shutil.rmtree(os.path.join(app6, "memories"))
items6 = oar.collect_items(app6, directive_min_hours=12)
check("hold still reported when other sources unreadable", len(items6), 1)
check("the surviving item is the hold", items6[0]["priority"], oar.P_HOLD)

# --- 7: hold is priority 0 (top of the list) when everything fires ---
print("--- 7: hold sorts first ---")
appx = make_app(hold="x", opreqs=[("OPREQ-Q", "OPEN")], directive="PENDING", directive_age_h=99)
check("hold first", oar.collect_items(appx, 12)[0]["priority"], oar.P_HOLD)

print()
if fail == 0:
    print("ALL PASS")
    sys.exit(0)
else:
    print("FAILURES")
    sys.exit(1)
