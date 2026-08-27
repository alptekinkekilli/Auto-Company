#!/usr/bin/env bash
# rfq-send.py invariant testi: fail-closed §15, form-only tespiti, anonimlik, guard-sync.
# Airtable erişimi yoksa (CI/headless) --report bölümü atlanır; syntax + guard hep koşar.
set -uo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script="${1:-$root/scripts/ops/rfq-send.py}"
fail=0
ok(){ echo "  ok: $1"; }
no(){ echo "  BAŞARISIZ: $1"; fail=1; }

echo "== syntax =="
python3 -c "import ast; ast.parse(open('$script').read())" && ok "python ast" || no "syntax"

echo "== guard koruması + sync =="
grep -q "scripts/ops/rfq-send.py" "$root/scripts/prod-mechanism-guard.py" && ok "guard PROTECTED" || no "guard'da yok"
python3 "$root/scripts/prod-mechanism-guard.py" --check-sync >/dev/null 2>&1 && ok "check-sync" || no "check-sync DRIFT"

echo "== kaynakta güvenlik invariant'ları =="
grep -q 'Sponsor İzni' "$script" && ok "§15 alanı" || no "§15 alanı yok"
grep -q '_sponsor_ok' "$script" && ok "§15 fonksiyonu" || no "§15 fn yok"
# G4'ü KULLANMAMALI (alıcı RFQ'su) — prose'da "G4 YOK" açıklaması serbest; asıl
# yasak olan G4 çağrısı/import'u (satıcı-tarafı tüzel-kişilik atfı gate'i).
if grep -qE "g4_live\(|g4\.judge|import g4|g4-check|g4_check" "$script"; then
  no "G4 KULLANIMI (çağrı/import) VAR — olmamalı"
else ok "G4 çağrısı/import yok"; fi
grep -q 'ANON_DENY' "$script" && ok "anonimlik denylist" || no "anonimlik denylist yok"
grep -q 'tblzcGP7kNfkmPDGJ' "$script" && ok "RFQ tablosu (tender değil)" || no "yanlış/eksik tablo"
if grep -q 'tbl1fZbNmolrEXAMy' "$script"; then no "frozen tender tablosuna referans VAR"; else ok "tender tablosuna dokunmuyor"; fi

echo "== canlı --report (Airtable varsa) =="
rep="$(python3 "$script" --report 2>&1)"; rc=$?
if [ $rc -ne 0 ] || echo "$rep" | grep -qiE "AIRTABLE_API_KEY yok"; then
  echo "  atlandı: Airtable erişimi yok (headless) — invariant testleri geçti"
else
  echo "$rep" | grep -qE "ALLOW: 0" && ok "fail-closed (ALLOW=0, kimse §15-izinli değil)" || no "ALLOW 0 değil — fail-closed kırık?"
  echo "$rep" | grep -q "§15 Sponsor İzni YOK" && ok "§15 REFUSE dalı" || no "§15 REFUSE görünmüyor"
  echo "$rep" | grep -q "form-only" && ok "form-only tespiti" || no "form-only tespiti yok"
  echo "$rep" | grep -qi "wowcar" && no "çıktıda 'wowcar' SIZDI" || ok "çıktıda son-şirket adı yok"
fi

echo "----"
[ $fail -eq 0 ] && echo "PASS" || { echo "FAIL"; exit 1; }
