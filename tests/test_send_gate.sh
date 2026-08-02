#!/usr/bin/env bash
# The send gate's refusal logic, offline.
#
#   bash tests/test_send_gate.sh
#
# From 2026-08-02 dispatch is autonomous: no human sees a message before it reaches a real
# company. These refusals are therefore the only thing between a bad row and a stranger's
# inbox, so what matters most is that every one of them FAILS CLOSED — an unknown must never
# come out the same door as an approval.
#
#   1. daily cap (3) and total cap (20) refuse, and the counts appear in the reason
#   2. a firm already contacted is refused — duplicate outreach is the most visible error
#   3. an opted-out firm is refused, detected at firm level across several fields
#   4. a non-Qualified status is refused
#   5. a missing/!malformed address is refused
#   6. TEST rows are excluded from the counts by STATUS, not by matching the word "test"
set -uo pipefail
cd "$(dirname "$0")/.."
SCRIPT=scripts/ops/send-gate.py
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: got '$2' want '$3'"; fail=1; fi; }
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }

# The decision is exercised with air()/g4_live() stubbed: the guards under test are pure
# policy, and a suite that needs the network is a suite nobody runs before committing.
run() {  # run <fields-json> <sent-rows-json> <g4-ok 0|1>
    python3 - "$SCRIPT" "$1" "$2" "$3" <<'PY'
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("sg", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
fields, sent, g4ok = json.loads(sys.argv[2]), json.loads(sys.argv[3]), sys.argv[4] == "1"
m.air = lambda path, params=None: (
    {"fields": fields} if "/" in path else
    {"records": [{"fields": f} for f in sent]})
m.g4_live = lambda firm, app: (g4ok, "PASS — stub" if g4ok else "HOLD — stub")
d = m.decide("recTEST", "/app")
print(d["verdict"] + "|" + d["reason"])
PY
}
OK='{"Business":"Test Firma Ltd","Status":"Qualified","Email":"info@example.com.tr"}'

echo "1. caps"
THREE='[{"Last contact date":"'"$(date -u +%Y-%m-%d)"'","Status":"Qualified"},{"Last contact date":"'"$(date -u +%Y-%m-%d)"'","Status":"Qualified"},{"Last contact date":"'"$(date -u +%Y-%m-%d)"'","Status":"Qualified"}]'
OUT=$(run "$OK" "$THREE" 1)
contains "daily cap refuses" "$OUT" "REFUSE"
contains "names the count" "$OUT" "3/3"
TWENTY=$(python3 -c "import json;print(json.dumps([{'Last contact date':'2026-07-01','Status':'Qualified'} for _ in range(20)]))")
OUT=$(run "$OK" "$TWENTY" 1)
contains "total cap refuses" "$OUT" "20/20"

echo "2. already contacted"
OUT=$(run '{"Business":"X","Status":"Qualified","Email":"a@b.tr","Last contact date":"2026-08-01"}' '[]' 1)
contains "refuses" "$OUT" "never send twice"

echo "3. opted out"
OUT=$(run '{"Business":"X","Status":"Qualified","Email":"a@b.tr","Notes":"firma opt-out istedi"}' '[]' 1)
contains "refuses" "$OUT" "opted out"

echo "4. not Qualified"
OUT=$(run '{"Business":"X","Status":"Held - Evidence insufficient","Email":"a@b.tr"}' '[]' 1)
contains "refuses" "$OUT" "not 'Qualified'"

echo "5. no usable address"
OUT=$(run '{"Business":"X","Status":"Qualified","Email":""}' '[]' 1)
contains "refuses" "$OUT" "no usable email"

echo "6. G4 failing refuses even when everything else is clean"
OUT=$(run "$OK" '[]' 0)
contains "refuses on G4" "$OUT" "G4 not verifiable"
check "clean row with G4 passing is allowed" "$(run "$OK" '[]' 1 | cut -d'|' -f1)" "ALLOW"

echo "7. TEST rows do not consume the caps"
# Excluded by STATUS: a real firm may legitimately have 'test' in its name.
TESTROWS='[{"Last contact date":"2026-08-01","Status":"TEST_COMPLETED / Archived"},{"Last contact date":"2026-08-01","Status":"TEST_PENDING"}]'
check "test rows ignored" "$(run "$OK" "$TESTROWS" 1 | cut -d'|' -f1)" "ALLOW"

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
