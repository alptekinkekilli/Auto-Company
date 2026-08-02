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
OK='{"Business":"Test Firma Ltd","Status":"Qualified","Email":"info@example.com.tr","Email subject":"konu","Email body":"<div>gövde</div>"}'

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

echo "8. an eligible but UNRENDERED row is refused"
# The first autonomous attempt (Rayelsis, 2026-08-02) was allowed against a row with no
# subject or body; the send path rejected it and wrote a Failed entry into the compliance
# log, which reached the operator as a delivery problem. Eligible != ready.
OUT=$(run '{"Business":"X","Status":"Qualified","Email":"a@b.tr"}' '[]' 1)
contains "refuses" "$OUT" "not ready to send"
contains "names the fields" "$OUT" "Email subject"
OUT=$(run '{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"s","Email body":"   "}' '[]' 1)
contains "whitespace body is still empty" "$OUT" "Email body"

echo "10. GROUP_ROUTED: allowed only when the body names the firm AND cites the decision"
# Operator decision 2026-08-02: a group mailbox can never satisfy strict G4, so the firm would
# be unreachable forever. Writing to the group while NAMING the bidding legal person and the
# karar no makes a misroute self-correcting instead of an accusation against the wrong company.
TITLE="MAGİM GRUP İNŞAAT-GIDA VE İHTİYAÇ MADDELERİ YATIRIM TİCARET LİMİTED ŞİRKETİ"
GR_OK=$(python3 -c "
import json
print(json.dumps({'Business':'Magim Grup','Status':'Qualified','Email':'ankara@magimgroup.com',
 'Email subject':'k','Outreach mode':'GROUP_ROUTED','Group domain':'magimgroup.com',
 'Registered title':'$TITLE','KIK exclusion ref':'2025/UY.II-2574 (İKN x)',
 'Email body':'... $TITLE ... 2025/UY.II-2574 ...'}))")
check "allowed with full evidence" "$(run "$GR_OK" '[]' 0 | cut -d'|' -f1)" "ALLOW"

# Each missing piece must refuse ON ITS OWN — G4 is stubbed FAILING throughout, so nothing
# here is being carried by the ordinary path.
NO_TITLE=$(python3 -c "
import json
print(json.dumps({'Business':'Magim Grup','Status':'Qualified','Email':'ankara@magimgroup.com',
 'Email subject':'k','Outreach mode':'GROUP_ROUTED','Group domain':'magimgroup.com',
 'Registered title':'$TITLE','KIK exclusion ref':'2025/UY.II-2574',
 'Email body':'sadece karar 2025/UY.II-2574 var, unvan yok'}))")
contains "refuses without the title" "$(run "$NO_TITLE" '[]' 0)" "FULL registered title"

NO_KARAR=$(python3 -c "
import json
print(json.dumps({'Business':'Magim Grup','Status':'Qualified','Email':'ankara@magimgroup.com',
 'Email subject':'k','Outreach mode':'GROUP_ROUTED','Group domain':'magimgroup.com',
 'Registered title':'$TITLE','KIK exclusion ref':'2025/UY.II-2574',
 'Email body':'... $TITLE ... karar numarasi yok'}))")
contains "refuses without the karar no" "$(run "$NO_KARAR" '[]' 0)" "karar no"

WRONG_DOM=$(python3 -c "
import json
print(json.dumps({'Business':'Magim Grup','Status':'Qualified','Email':'bilgi@baskasite.com',
 'Email subject':'k','Outreach mode':'GROUP_ROUTED','Group domain':'magimgroup.com',
 'Registered title':'$TITLE','KIK exclusion ref':'2025/UY.II-2574',
 'Email body':'... $TITLE ... 2025/UY.II-2574 ...'}))")
contains "refuses an off-group recipient" "$(run "$WRONG_DOM" '[]' 0)" "not first-party on the group domain"

echo "11. GROUP_ROUTED does not lift the caps"
check "daily cap still binds" "$(run "$GR_OK" "$THREE" 0 | cut -d'|' -f1)" "REFUSE"

echo "12. a row that disagrees with itself is refused"
# Arkenom, 2026-08-02: Status "Qualified" while Notes said "MOVED TO HELD" — and the firm had
# already been emailed. Keying on Status alone let the row pass while contradicting itself.
CONTRA=$(python3 -c "
import json
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'g','Notes':'G4 RE-VERIFICATION FAILED ... MOVED TO HELD'}))")
contains "refuses" "$(run "$CONTRA" '[]' 1)" "disagrees with itself"
contains "names the remedy" "$(run "$CONTRA" '[]' 1)" "G4 RESOLVED"

RESOLVED=$(python3 -c "
import json
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'g','Notes':'G4 RE-VERIFICATION FAILED ... MOVED TO HELD\n\nG4 RESOLVED 2026-08-02: render-first, refuted.'}))")
check "a stamped resolution clears it" "$(run "$RESOLVED" '[]' 1 | cut -d'|' -f1)" "ALLOW"

STALE_STAMP=$(python3 -c "
import json
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'g','Notes':'G4 RESOLVED 2026-07-01\n\nG4 RE-VERIFICATION FAILED ... MOVED TO HELD'}))")
contains "an OLDER stamp does not clear a NEWER hold" "$(run "$STALE_STAMP" '[]' 1)" "disagrees with itself"

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
