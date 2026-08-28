#!/usr/bin/env bash
# RFQ yanıt-bildiricisi regresyon testi (scripts/ops/rfq-reply-watch.py).
#
#   bash tests/test_rfq_reply_watch.sh
#
# Pinlenen yargı: gönderilmiş bir RFQ satırı yanıt alırsa BİR KEZ bildirilir; sessizlik
# yaşıyla birlikte GÖZLEM olarak bildirilir, hüküm olmaz; yanıt veren satır asla "sessiz"
# sayılmaz. Ayrıca INVARIANT'lar: advisory (Airtable'a YAZMAZ), doğru tablo (RFQ, tender
# DEĞİL), ve tender-satıcı dili (İKN/Stage 2) SIZMAZ (anonimlik/alıcı-rolü).
set -uo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${1:-$root/scripts/ops/rfq-reply-watch.py}"
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in output"; fail=1 ;; esac; }
absent()   { case "$2" in *"$3"*) echo "  FAIL $1: unexpected '$3'"; fail=1 ;; *) echo "  PASS $1" ;; esac; }
ok(){ echo "  PASS $1"; }
no(){ echo "  FAIL $1"; fail=1; }

echo "== kaynak invariant'ları =="
python3 -c "import ast; ast.parse(open('$SCRIPT').read())" && ok "python ast" || no "syntax"
grep -q 'tblzcGP7kNfkmPDGJ' "$SCRIPT" && ok "RFQ tablosu (tender değil)" || no "yanlış/eksik tablo"
if grep -q 'tbl1fZbNmolrEXAMy' "$SCRIPT"; then no "frozen tender tablosuna referans VAR"; else ok "tender tablosuna dokunmuyor"; fi
# Advisory: hiçbir mutasyon HTTP metodu kullanmamalı (yalnız GET okur).
if grep -qE 'method="(PATCH|POST|PUT|DELETE)"|"PATCH"|updateRecord|_mark_' "$SCRIPT"; then
  no "YAZMA yolu (PATCH/POST) VAR — advisory olmalı"
else ok "advisory (yazma yolu yok)"; fi

WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/logs"
# rfq-send.py 'Gönderim TS'yi UTC '%Y-%m-%dT%H:%M' (tz'siz) yazar — fixture aynı biçimi kullanır.
NOW=$(python3 -c "import datetime;print(datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M'))")
OLD=$(python3 -c "import datetime;print((datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=100)).strftime('%Y-%m-%dT%H:%M'))")
RLOG_TS=$(python3 -c "import datetime;print(datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'))")

python3 - "$WORK/rows.json" "$NOW" "$OLD" "$RLOG_TS" <<'PY'
import json, sys
out, now, old, rlog_ts = sys.argv[1:5]
rows = [
 # Yanıt gelmiş + eski gönderim: yalnız REPLY (asla "sessiz" değil).
 {"id": "recREPLY", "fields": {"Firma": "Cevap Veren Broker", "Küme": "Sigorta",
  "Durum": "Gönderildi", "Gönderim TS": old,
  "Reply log": "[%s] teklif@cevapveren.com: Kasko + trafik icin indikatif fiyati ekte gonderdik" % rlog_ts}},
 # Taze gönderim: eşik altında → hiçbir şey.
 {"id": "recFRESH", "fields": {"Firma": "Yeni Gonderim Bulut", "Küme": "Bulut & Güvenlik",
  "Durum": "Gönderildi", "Gönderim TS": now}},
 # Eski gönderim, yanıt yok → SESSİZLİK (yaşıyla, bir kez).
 {"id": "recSILENT", "fields": {"Firma": "Sessiz ERP", "Küme": "ERP + e-Fatura",
  "Durum": "Gönderildi", "Gönderim TS": old}},
]
open(out, "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False))
PY

run() { python3 "$SCRIPT" --app "$WORK" --fixture "$WORK/rows.json" --silence-hours 72 "$@" 2>&1; }

echo "== 1. karışık fixture ilk geçiş =="
OUT=$(run)
contains "counts"           "$OUT" "sent_rows=3 new_replies=1 newly_silent=1"
contains "reply reported"   "$OUT" "Cevap Veren Broker"
contains "reply küme"       "$OUT" "Sigorta"
contains "reply content"    "$OUT" "indikatif fiyati"
contains "reply→OPEX yönlendirme" "$OUT" "OPEX mutabakat"
contains "silence"          "$OUT" "Sessiz ERP"
absent   "fresh row quiet"  "$OUT" "Yeni Gonderim"
# Yanıt veren satır 100 saat eski: asla "sessiz" listesine girmemeli.
absent   "replied != silent" "$OUT" "Cevap Veren Broker [Sigorta] (100"

echo "== 2. anonimlik/alıcı-rolü: tender-satıcı dili SIZMAMALI =="
absent   "no İKN language"   "$OUT" "İKN"
absent   "no Stage 2"        "$OUT" "Stage 2"

echo "== 3. sessizlik bir gözlem, hüküm değil =="
contains "no verdict"       "$OUT" "hüküm değil"

echo "== 4. state ikinci uyarıyı bastırır =="
OUT2=$(run)
contains "nothing new"      "$OUT2" "new_replies=0 newly_silent=0"
contains "silent run"       "$OUT2" "no new RFQ outcomes"

echo "== 5. --dry-run state bırakmaz =="
rm -f "$WORK/logs/rfq-reply-watch-state.json"
run --dry-run >/dev/null
if [ -f "$WORK/logs/rfq-reply-watch-state.json" ]; then
    no "dry-run state yazdı"
else
    ok "dry-run state yazmadı"
fi

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
