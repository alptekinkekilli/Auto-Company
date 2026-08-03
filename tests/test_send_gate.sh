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
run() {  # run <fields-json> <sent-rows-json> <g4-ok 0|1> [followup 0|1]
    python3 - "$SCRIPT" "$1" "$2" "$3" "${4:-0}" <<'PY'
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("sg", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
fields, sent, g4ok = json.loads(sys.argv[2]), json.loads(sys.argv[3]), sys.argv[4] == "1"
followup = sys.argv[5] == "1"
m.air = lambda path, params=None: (
    {"fields": fields} if "/" in path else
    {"records": [{"fields": f} for f in sent]})
m.g4_live = lambda firm, app, outreach_website="": (g4ok, "PASS — stub" if g4ok else "HOLD — stub")
d = m.decide("recTEST", "/app", followup=followup)
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

echo "13. an Exclusion ground unfit to send verbatim is refused"
# N.K.Y, 2026-08-02: the field doubles as an internal research note and is interpolated into
# the customer's Turkish sentence as-is. 1,234 chars of English analysis went out, including a
# parenthetical inference about a DIFFERENT company. Healthy grounds measured 50-204 chars, 0
# English markers.
LONG_EN='As özel ortak (special/minority partner) of JV, N.K.Y own submitted foreign iş deneyim belgesi had a defective apostil chain and the other submitted documents did not independently meet the required amount. Both defects are attributed by name specifically to N.K.Y and were not attributed to the pilot partner by implication.'
BAD=$(python3 -c "
import json,sys
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'g','Exclusion ground':sys.argv[1]}))" "$LONG_EN")
contains "refuses" "$(run "$BAD" '[]' 1)" "not fit to send verbatim"
contains "reports the measurements" "$(run "$BAD" '[]' 1)" "English markers"

GOOD=$(python3 -c "
import json
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'g','Exclusion ground':'aşırı düşük teklif açıklamasının tevsik yöntemi mevzuata uygun değil'}))")
check "a short Turkish ground passes" "$(run "$GOOD" '[]' 1 | cut -d'|' -f1)" "ALLOW"

echo "14. procurement phase must match the authority's own decision"
# N.K.Y (2025/UD.I-1751) was eliminated at ÖN YETERLİK — nobody had bid yet — but the approved
# template says "teklif değerlendirilmeden önce" and "değerlendirme dışı bırakıldığını gördüm".
# That message went to a real firm on 2026-08-02 and told it the wrong thing about its own file.
# The strings below are the operative wording of the two real decisions.
PH='import importlib.util,sys
spec=importlib.util.spec_from_file_location("sg",sys.argv[1])
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.phase_of(sys.argv[2]) if sys.argv[3]=="d" else m.body_claims(sys.argv[2]))'
ph() { python3 -c "$PH" "$SCRIPT" "$1" d; }
bc() { python3 -c "$PH" "$SCRIPT" "$1" b; }

NKY_DEC='Sonuc olarak, Apco Teknik Grup - N.K.Y Mimarlik Is Ortakliginin ön yeterlik basvurusunun yeterli kabul edilmeyerek ön yeterlik degerlendirmesi disinda birakilmasi gerekmektedir.'
RMH_DEC='Sonuc olarak, Abe Biyosidal ile Rmh Ilac Kimya San. ve Tic. Ltd. Sti.nin tekliflerinin değerlendirme dışı bırakılması gerekmektedir.'
check "ön yeterlik decision reads PREQUAL"   "$(ph "$NKY_DEC")" "PREQUAL"
check "bid decision reads BID"               "$(ph "$RMH_DEC")" "BID"
check "an unreadable decision is UNKNOWN"    "$(ph "")" "UNKNOWN"
check "the template body claims BID"         "$(bc 'gerekçesiyle değerlendirme dışı bırakıldığını gördüm')" "BID"
check "a prequal-worded body claims PREQUAL" "$(bc 'ön yeterlik değerlendirmesi dışında bırakıldığını gördüm')" "PREQUAL"
if [ "$(ph "$NKY_DEC")" != "$(bc 'gerekçesiyle değerlendirme dışı bırakıldığını gördüm')" ]; then
  echo "  PASS the exact N.K.Y pairing is detected as a mismatch"
else
  echo "  FAIL the N.K.Y pairing was not detected"; fail=1
fi

echo "15. body leak scanner (directive 2026-08-02 rev 3, N.K.Y incident 2026-08-02T15:01Z)"
# The N.K.Y message that actually went out carried the company's own internal reasoning
# into a stranger's inbox: which agent ruled what, a deliberate row-creation decision, method
# notes. This is the exact body that shipped — loaded from a fixture so the test asserts
# against the real incident, not a paraphrase of it.
NKY_ROW=$(python3 -c "
import json
body = json.load(open('tests/fixtures/nky_actual_sent_body.json'))['Email body']
print(json.dumps({'Business':'N.K.Y Mimarlık Müh. İnş. ve Tic. Ltd. Şti.','Status':'Qualified',
 'Email':'info@nky.com.tr','Email subject':'s','Email body':body,
 'Exclusion ground':'As özel ortak of the JV, an ordinary remediable documentary defect, m.54/11-b corrective measure.'}))")
OUT=$(run "$NKY_ROW" '[]' 1)
contains "refuses the actual sent body" "$OUT" "REFUSE"
contains "names critic-munger" "$OUT" "munger"

echo "  a clean authority-only body does not fire (a scanner that refuses everything is an outage)"
CLEAN_BODY_ROW=$(python3 -c "
import json
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'Kamuya açık KİK kurul kararında, X firmasının bilanço oranlarının uygun olmaması nedeniyle değerlendirme dışı bırakıldığını gördüm.',
 'Exclusion ground':'bilanço oranlarının uygun olmaması (mali yeterlik)'}))")
check "clean body is allowed" "$(run "$CLEAN_BODY_ROW" '[]' 1 | cut -d'|' -f1)" "ALLOW"

echo "  one case per marker class"
mkcase() { python3 -c "
import json, sys
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':sys.argv[1], 'Exclusion ground':'temiz gerekçe metni'}))" "$1"; }
contains "persona name (bezos)" "$(run "$(mkcase 'ceo-bezos onayladı bu metni')" '[]' 1)" "REFUSE"
contains "verdict vocabulary (PASS WITH CONDITIONS)" "$(run "$(mkcase 'critic ruled PASS WITH CONDITIONS on this row')" '[]' 1)" "REFUSE"
contains "verdict vocabulary (OPREQ)" "$(run "$(mkcase 'see OPREQ-208A-001 for context')" '[]' 1)" "REFUSE"
contains "method/provenance (sha256:)" "$(run "$(mkcase 'verified via sha256:abcdef1234567890')" '[]' 1)" "REFUSE"
contains "method/provenance (Category 2)" "$(run "$(mkcase 'this is a Category 2 finding')" '[]' 1)" "REFUSE"
contains "internal phrasing (Deliberately NOT)" "$(run "$(mkcase 'Deliberately NOT creating a row for the partner')" '[]' 1)" "REFUSE"
contains "internal phrasing (not a usable pitch)" "$(run "$(mkcase 'this is not a usable pitch to the partner')" '[]' 1)" "REFUSE"

echo "  a scanner refusal names the marker it hit, not a bare 'leak found'"
OUT=$(run "$(mkcase 'ceo-bezos onayladı')" '[]' 1)
contains "names the exact marker" "$OUT" "bezos"

echo "16. an UNSPLIT row (leak still in Exclusion ground, body not yet re-rendered) is refused"
# A half-finished migration: Exclusion ground still carries the internal marker even though
# nobody has re-rendered Email body from it yet. The source-field guard must catch this too.
UNSPLIT=$(python3 -c "
import json
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'temiz görünen bir metin, henüz yeniden render edilmedi',
 'Exclusion ground':'ordinary defect — critic-munger PASS WITH CONDITIONS confirmed this'}))")
contains "refuses" "$(run "$UNSPLIT" '[]' 1)" "not split yet"

echo "17. follow-up mode (directive rev 4 §3): at most one authorized second contact"
# Without --followup, a row with Last contact date is refused exactly as before, unchanged.
SENT_ONCE='{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"k","Email body":"g","Last contact date":"2026-08-01"}'
contains "non-followup mode still refuses a second first-contact" "$(run "$SENT_ONCE" '[]' 1 0)" "never send twice"

# In --followup mode, a row that was actually sent once is now allowed.
check "followup mode allows an already-sent Qualified row" "$(run "$SENT_ONCE" '[]' 1 1 | cut -d'|' -f1)" "ALLOW"
contains "reason is labeled FOLLOW-UP" "$(run "$SENT_ONCE" '[]' 1 1)" "FOLLOW-UP:"

# A row with no Last contact date has nothing to follow up.
NEVER_SENT='{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"k","Email body":"g"}'
contains "followup mode refuses a row never sent" "$(run "$NEVER_SENT" '[]' 1 1)" "nothing to follow up"

# A row whose Contact attempts is already 2 (first send + a follow-up) is refused a second follow-up.
ALREADY_FOLLOWED='{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"k","Email body":"g","Last contact date":"2026-08-01","Contact attempts":2}'
contains "followup mode refuses a second follow-up" "$(run "$ALREADY_FOLLOWED" '[]' 1 1)" "already sent on this row"

# Follow-up mode does not bypass any other gate — caps, opt-out, body leak scan all still bind.
contains "followup mode still respects the daily cap" "$(run "$SENT_ONCE" "$THREE" 1 1)" "daily cap reached"
OPTOUT_SENT='{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"k","Email body":"g","Last contact date":"2026-08-01","Notes":"firma opt-out istedi"}'
contains "followup mode still refuses an opted-out firm" "$(run "$OPTOUT_SENT" '[]' 1 1)" "opted out"
LEAKY_FOLLOWUP=$(python3 -c "
import json
print(json.dumps({'Business':'X','Status':'Qualified','Email':'a@b.tr','Email subject':'k',
 'Email body':'ceo-bezos onayladı bu metni','Last contact date':'2026-08-01'}))")
contains "followup mode still runs the body leak scan" "$(run "$LEAKY_FOLLOWUP" '[]' 1 1)" "REFUSE"

echo "18. g4_live firm-name matching (cycle 77 bug: single-longest-word token match let two"
echo "    different firms sharing a word collide; only an exact normalized-name match is safe)"
run_g4live() {  # run_g4live <firm> <bridge-rows-json>
    # Bridge rows here carry no domain/address fields, so if the name-match passes, control
    # reaches the real g4.judge() with no candidate domain -> a fast HOLD, no network call.
    # That is enough to prove PAST the name-matching guard vs. REFUSED BY it.
    python3 - "$SCRIPT" "$1" "$2" <<'PY'
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("sg", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
firm, rows = sys.argv[2], json.loads(sys.argv[3])
m.air = lambda path, params=None: {"records": [{"fields": f} for f in rows]}
ok, why = m.g4_live(firm, "/app")
print(("ALLOW" if ok else "REFUSE") + "|" + why)
PY
}
# Two different firms whose full names both contain the token "Teknolojileri" — this is the
# exact collision that produced a false ALLOW on Bilgi Birikim using Rayelsis's evidence.
BRIDGE_ROWS='[{"firm":"Rayelsis Elektronik Elektromekanik Danışmanlık Müşavirlik Lojistik ve Raylı Sistem Teknolojileri Sanayi Ticaret Limited Şirketi"}]'
OUT=$(run_g4live "Bilgi Birikim Sistemleri Bilişim Teknolojileri Anonim Şirketi" "$BRIDGE_ROWS")
contains "different firm sharing the longest token is refused, not matched" "$OUT" "no exact firm-name match"
OUT=$(run_g4live "Rayelsis Elektronik Elektromekanik Danışmanlık Müşavirlik Lojistik ve Raylı Sistem Teknolojileri Sanayi Ticaret Limited Şirketi" "$BRIDGE_ROWS")
case "$OUT" in *"no exact firm-name match"*) echo "  FAIL exact match should not report name-mismatch: $OUT"; fail=1 ;; *) echo "  PASS exact match bypasses the name-mismatch refusal (reaches judge(), gets a fast no-domain HOLD)" ;; esac
# Case/whitespace differences between the row and the query should still count as exact.
BRIDGE_ROWS2='[{"firm":"  Bilgi Birikim Sistemleri   Bilişim Teknolojileri Anonim Şirketi  "}]'
OUT=$(run_g4live "Bilgi Birikim Sistemleri Bilişim Teknolojileri Anonim Şirketi" "$BRIDGE_ROWS2")
case "$OUT" in *"no exact firm-name match"*) echo "  FAIL should normalize whitespace: $OUT"; fail=1 ;; *) echo "  PASS whitespace-normalized name still counts as exact" ;; esac

echo "19. g4_live falls back to the Outreach row's own Website field only when the exact-"
echo "    matched bridge row names no domain of its own (cycle 82, Bilgi Birikim gap)"
run_g4live_web() {  # run_g4live_web <firm> <bridge-rows-json> <outreach-website>
    python3 - "$SCRIPT" "$1" "$2" "$3" <<'PY'
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("sg", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
firm, rows, website = sys.argv[2], json.loads(sys.argv[3]), sys.argv[4]
m.air = lambda path, params=None: {"records": [{"fields": f} for f in rows]}
# g4_live() loads g4-check.py fresh via importlib.util.module_from_spec every call. Wrap that
# function so that, for exactly the "g4" spec it requests, the real domains_in() still runs
# (that is what decides whether the fallback should even trigger) but judge() is replaced with
# a stub that just echoes back whatever domain it was actually given — the one thing this test
# needs to observe.
def stub_judge(fields, domain_override, mcp):
    return {"verdict": "HOLD", "reason": "stub sees domain=%r" % domain_override}
orig_module_from_spec = importlib.util.module_from_spec
def wrapped(spec2):
    mod = orig_module_from_spec(spec2)
    if spec2.name == "g4":
        orig_exec = spec2.loader.exec_module
        def exec_and_patch(mm):
            orig_exec(mm)
            mm.judge = stub_judge
        spec2.loader.exec_module = exec_and_patch
    return mod
importlib.util.module_from_spec = wrapped
ok, why = m.g4_live(firm, "/app", outreach_website=website)
print(("ALLOW" if ok else "REFUSE") + "|" + why)
PY
}
NO_DOMAIN_ROW='[{"firm":"Bilgi Birikim Sistemleri Bilişim Teknolojileri Anonim Şirketi","result_data":"MERSİS No: 0172082863000001 | Firma Durumu: Aktif"}]'
OUT=$(run_g4live_web "Bilgi Birikim Sistemleri Bilişim Teknolojileri Anonim Şirketi" "$NO_DOMAIN_ROW" "https://www.bilgibirikim.com/")
contains "bridge row with no domain uses the Outreach row's Website as fallback" "$OUT" "domain='bilgibirikim.com'"
contains "reason names the fallback source" "$OUT" "Outreach row's Website field"
HAS_DOMAIN_ROW='[{"firm":"Essa Enerji Sistemleri Sanayi ve Ticaret Anonim Şirketi","result_data":"Site: https://essaenerji.com.tr | Adres: X"}]'
OUT=$(run_g4live_web "Essa Enerji Sistemleri Sanayi ve Ticaret Anonim Şirketi" "$HAS_DOMAIN_ROW" "https://www.somethingelse.com.tr/")
contains "bridge row that already names a domain is never overridden by the fallback" "$OUT" "domain=''"
OUT=$(run_g4live_web "Bilgi Birikim Sistemleri Bilişim Teknolojileri Anonim Şirketi" "$NO_DOMAIN_ROW" "")
contains "no Outreach website given: no fallback applied, domain stays empty" "$OUT" "domain=''"

echo "20. phase check is scoped to first-contact sends only (cycle 86 fix)"
echo "    the approved Step-2 template asserts no procurement phase, so body_claims() on any"
echo "    real follow-up body is always UNKNOWN — which used to REFUSE every follow-up"
echo "    unconditionally, not because the message said the wrong stage but because it made"
echo "    no claim to check. N.K.Y (cycle 81) and Bilgi Birikim (cycle 82) both hit this."
PHASE_FIELDS='{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"k",
 "Email body":"lutfen IKN ile yanit verin","Exclusion ground":"kisa turkce gerekce",
 "Exclusion ground source":"KararId=deadbeef00000000000000000000000000000000000000000000000000000001",
 "Last contact date":"2026-08-01","Contact attempts":1}'
OUT=$(run "$PHASE_FIELDS" '[]' 1 1)
case "$OUT" in
  *"could not read the decision"*) echo "  FAIL follow-up still attempted the phase fetch: $OUT"; fail=1 ;;
  *"phase mismatch"*) echo "  FAIL follow-up still ran the phase-mismatch check: $OUT"; fail=1 ;;
  *) echo "  PASS follow-up skips the phase check entirely (no fetch attempted, no mismatch reported)" ;;
esac
# First-contact sends must still be checked exactly as before: no network in this offline
# suite means the fetch will fail, and that failure must still be a REFUSE (fail-closed).
PHASE_FIELDS_FIRST='{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"k",
 "Email body":"lutfen IKN ile yanit verin","Exclusion ground":"kisa turkce gerekce",
 "Exclusion ground source":"KararId=deadbeef00000000000000000000000000000000000000000000000000000001"}'
OUT=$(run "$PHASE_FIELDS_FIRST" '[]' 1 0)
case "$OUT" in
  *"could not read the decision"*|*"cannot tell from the decision"*)
    echo "  PASS first-contact sends still run the phase check (fails closed here since no network)" ;;
  *) echo "  FAIL first-contact phase check did not fail closed: $OUT"; fail=1 ;;
esac

echo "21. opted_out() catches the mail provider's literal wording (cycle 89: Bilgi Birikim's"
echo "    follow-up was suppressed 2026-08-03T13:25:46Z with Email log 'Suppressed: Recipient"
echo "    has opted out' -- the old check tested 'opt-out'/'opt out' but not 'opted out')"
OPTED_OUT_LOG='{"Business":"X","Status":"Qualified","Email":"a@b.tr","Email subject":"k",
 "Email body":"g","Last contact date":"2026-08-01",
 "Email log":"[2026-08-03T13:25:46.855Z] Suppressed: Recipient has opted out\n[2026-08-01T20:26:46.791Z] Sent: Sent (1/15 today)"}'
contains "refuses a row whose Email log records provider-side opt-out" \
  "$(run "$OPTED_OUT_LOG" '[]' 1 1)" "opted out"

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
