#!/usr/bin/env bash
# The G4 attribution checker's decision logic, exercised offline.
#
#   bash tests/test_g4_check.sh
#
# Only the pure functions are testable without the network — and they are the ones that
# decide. The address matcher is the whole tool: too loose and it fires on any Turkish
# address ("MAH SK NO" appears in all of them), too strict and the register's abbreviations
# never meet a website's spelled-out words. Both failure modes were live risks on the
# RAYELSİS row, whose register says "YENİ BATI MAH. 2374 SK. NO: 3" while its site says
# "Yeni Batı Mahallesi 2374 Sokak No: 3".
#
#   1. register abbreviations match a site's spelled-out address
#   2. Turkish dotted/dotless İ-I folding does not break the match
#   3. a DIFFERENT address on the same street pattern does NOT match (the coincidence guard)
#   4. the third-party-directory address that conflicts with the register does NOT match
#   5. a MERSİS number printed on the site is an accepted anchor, with or without spacing
#   6. domain extraction skips authority sources (kik.gov.tr, mersis) and keeps the firm's own
set -uo pipefail
cd "$(dirname "$0")/.."
SCRIPT=scripts/ops/g4-check.py
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: got '$2' want '$3'"; fail=1; fi; }

py() { python3 - "$SCRIPT" "$@" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("g4", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
op = sys.argv[2]
if op == "addr":
    ok, _ = m.address_anchor(sys.argv[3], sys.argv[4]); print("yes" if ok else "no")
elif op == "id":
    ok, _ = m.registry_id_anchor(sys.argv[3], sys.argv[4]); print("yes" if ok else "no")
elif op == "dom":
    print(",".join(m.domains_in(sys.argv[3])))
PY
}

REG="YENİ BATI MAH. 2374 SK. NO: 3 YENİMAHALLE / ANKARA"

echo "1. register abbreviations vs a site's spelled-out address"
check "matches" "$(py addr "$REG" 'Yeni Batı Mahallesi 2374 Sokak No: 3 06370 Yenimahalle - Ankara / TURKEY')" "yes"

echo "2. Turkish İ/ı folding does not break it"
check "matches lowercase dotless" "$(py addr "$REG" 'yeni batı mahallesi 2374 sokak no 3 yenimahalle ankara')" "yes"

echo "3. a different address on the same street pattern is rejected"
# Same boilerplate words, different numbers and mahalle: this must NOT be an anchor, or the
# matcher would confirm every Turkish address it is ever shown.
check "rejects" "$(py addr "$REG" 'Cumhuriyet Mahallesi 118 Sokak No: 42 Çankaya - Ankara')" "no"

echo "4. the conflicting directory address is rejected"
# The real trap: a third-party directory gave this for RAYELSİS while the register says
# Yeni Batı. Anchoring on it would have attributed the firm to the wrong address.
check "rejects directory address" "$(py addr "$REG" 'İvedikköy Mah. 1495. Sokak No:17/55 Yenimahalle-Ankara')" "no"

echo "5. a MERSİS number on the site is an accepted anchor"
check "plain" "$(py id 'MERSİS No: 0734225615100001' 'Mersis No 0734225615100001')" "yes"
check "spaced/punctuated" "$(py id 'MERSİS No: 0734225615100001' 'MERSIS: 0734-2256-1510-0001')" "yes"
check "absent" "$(py id 'MERSİS No: 0734225615100001' 'no registry number here at all')" "no"

echo "6. domain extraction ignores authority sources"
check "keeps firm site only" \
  "$(py dom 'site https://rayelsis.com/iletisim ve karar https://ekap.kik.gov.tr/EKAP/Vatandas/X kaynak https://mersis.ticaret.gov.tr/y')" \
  "rayelsis.com"

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
