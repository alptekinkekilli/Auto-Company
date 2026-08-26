#!/usr/bin/env bash
# compact ritüeli sertleştirme testleri:
#   1) compact-preflight.py'nin resume_durumu() YALNIZ mtime değil,
#      compact-resume-lint.py'yi de koşturup "taze" derken içeriği doğruluyor mu
#      (asıl kaçak buradaydı: mtime taze ama içerik bozuk resume'lar geçiyordu).
#   2) scripts/compact-postcheck.py — resume ankorlarının compact_summary içinde
#      görünüp görünmediğini doğru hesaplayıp log'a doğru JSON satırı yazıyor mu.
#
# İki script de COMPACT_RESUME_PATH/COMPACT_BLOCK_MARKER/COMPACT_HISTORY_LOG
# env override'larıyla test edilir — gerçek /tmp/compact-resume.md'ye ASLA
# dokunulmaz (o dosya kullanıcının kanonik, canlı resume'u olabilir).
#
#   bash tests/test_compact_ritual_hardening.sh
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected exit $3 got $2"; fail=1; fi; }
check_has() { if echo "$2" | grep -qF "$3"; then echo "  PASS $1"; else echo "  FAIL $1: beklenen alt-dize yok: $3"; fail=1; fi; }
check_not_has() { if echo "$2" | grep -qF "$3"; then echo "  FAIL $1: BEKLENMEYEN alt-dize var: $3"; fail=1; else echo "  PASS $1"; fi; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT
RESUME_OK="$SB/resume-ok.md"
RESUME_BAD="$SB/resume-bad.md"
MARKER="$SB/marker"
LOG="$SB/history.log"

# Lint'i gerçekten geçen minimal bir resume (zorunlu bölümler + sayısız).
cat >"$RESUME_OK" <<'EOF'
# RESUME — test

## İLK İŞ
- ilk adım

## KARARLAR
- karar metni

## DOĞRULANMIŞ / DOĞRULANMAMIŞ
- DOĞRULANMIŞ: ölçüldü
- DOĞRULANMAMIŞ: yok

## BEKLEYEN KULLANICI KARARI
- yok

## İZLEYİCİLER
- yok
EOF

# Lint'i İHLAL eden bir resume (para tutarı taşıyor — YASAK deseni).
cat >"$RESUME_BAD" <<'EOF'
# RESUME — test

## İLK İŞ
- bugün $150 harcandı, tavan yakın

## KARARLAR
- karar metni

## DOĞRULANMIŞ / DOĞRULANMAMIŞ
- DOĞRULANMIŞ: ölçüldü
- DOĞRULANMAMIŞ: yok

## BEKLEYEN KULLANICI KARARI
- yok

## İZLEYİCİLER
- yok
EOF

echo "== compact-resume-lint.py sanity =="
r=$(python3 scripts/compact-resume-lint.py "$RESUME_OK" >/dev/null 2>&1; echo $?)
check "1 iyi resume lint yesil" "$r" 0
r=$(python3 scripts/compact-resume-lint.py "$RESUME_BAD" >/dev/null 2>&1; echo $?)
check "2 kotu resume lint kirmizi" "$r" 1

echo "== compact-preflight.py: lint-gated freshness =="
out=$(echo '{"trigger":"manual"}' | COMPACT_RESUME_PATH="$RESUME_OK" COMPACT_BLOCK_MARKER="$MARKER" python3 scripts/compact-preflight.py 2>/dev/null)
check_not_has "3 taze+lint-yesil resume icin uyari YOK" "$out" "RESUME DOSYASI"

out=$(echo '{"trigger":"manual"}' | COMPACT_RESUME_PATH="$RESUME_BAD" COMPACT_BLOCK_MARKER="$MARKER" python3 scripts/compact-preflight.py 2>/dev/null)
check_has "4 taze-ama-lint-kirmizi artik BAYAT sayilir" "$out" "RESUME DOSYASI"
check_has "5 gerekce LINT KIRMIZI iceriyor" "$out" "LINT KIRMIZI"

out=$(echo '{"trigger":"manual"}' | COMPACT_RESUME_PATH="$SB/yok-boyle-dosya.md" COMPACT_BLOCK_MARKER="$MARKER" python3 scripts/compact-preflight.py 2>/dev/null)
check_has "6 dosya yoksa acik mesaj" "$out" "resume dosyası YOK"

# mtime'ı geriye al (bayat) — eski davranış regresyon koruması.
STALE="$SB/resume-stale.md"; cp "$RESUME_OK" "$STALE"
python3 - "$STALE" <<'PY'
import os, sys, time
os.utime(sys.argv[1], (time.time() - 4 * 3600,) * 2)
PY
out=$(echo '{"trigger":"manual"}' | COMPACT_RESUME_PATH="$STALE" COMPACT_BLOCK_MARKER="$MARKER" python3 scripts/compact-preflight.py 2>/dev/null)
check_has "7 mtime bayat (3sa ustu) BAYAT mesaji" "$out" "BAYAT"

echo "== compact-preflight.py: auto-block tek atis =="
rm -f "$MARKER"
out=$(echo '{"trigger":"auto"}' | COMPACT_RESUME_PATH="$SB/yok.md" COMPACT_BLOCK_MARKER="$MARKER" python3 scripts/compact-preflight.py 2>/dev/null)
check_has "8 auto+resume-yok -> block JSON" "$out" '"decision": "block"'
py_ok=$(echo "$out" | python3 -c "import json,sys; json.loads(sys.stdin.read()); print('SAF')" 2>/dev/null)
check_has "9 block ciktisi SAF JSON (markdown karismamis)" "$py_ok" "SAF"
out=$(echo '{"trigger":"auto"}' | COMPACT_RESUME_PATH="$SB/yok.md" COMPACT_BLOCK_MARKER="$MARKER" python3 scripts/compact-preflight.py 2>/dev/null)
check_not_has "10 taze marker ile ikinci auto GECER" "$out" '"decision": "block"'
out=$(echo '{"trigger":"manual"}' | COMPACT_RESUME_PATH="$SB/yok.md" COMPACT_BLOCK_MARKER="$SB/m2" python3 scripts/compact-preflight.py 2>/dev/null)
check_not_has "11 manuel compact ASLA bloklanmaz" "$out" '"decision": "block"'
out=$(echo '{"trigger":"auto"}' | COMPACT_AUTOBLOCK=0 COMPACT_RESUME_PATH="$SB/yok.md" COMPACT_BLOCK_MARKER="$SB/m3" python3 scripts/compact-preflight.py 2>/dev/null)
check_not_has "12 COMPACT_AUTOBLOCK=0 kapatir" "$out" '"decision": "block"'

echo "== compact-postcheck.py =="
out=$(printf '{"trigger":"manual","compact_summary":"Ozet metni: ILK IS ve KARAR gecer, digerleri gecmez"}' \
  | COMPACT_RESUME_PATH="$RESUME_OK" COMPACT_HISTORY_LOG="$LOG" python3 scripts/compact-postcheck.py)
r=$?
check "13 gecerli payload exit 0" "$r" 0
check_has "14 kanarya uyarisi basildi" "$out" "kanarya"
last=$(tail -1 "$LOG")
check_has "15 log satiri yazildi" "$last" "\"trigger\": \"manual\""
check_has "16 kayip_ankorlar dolu" "$last" "kayip_ankorlar"

out=$(printf '{"trigger":"manual","compact_summary":"İLK İŞ, KARAR, DOĞRULANMAMIŞ, BEKLEYEN, İZLEYİCİ hepsi burada"}' \
  | COMPACT_RESUME_PATH="$RESUME_OK" COMPACT_HISTORY_LOG="$LOG" python3 scripts/compact-postcheck.py)
r=$?
check "17 tam-kapsama payload exit 0" "$r" 0
check_not_has "18 tam kapsamada kanarya uyarisi YOK" "$out" "kanarya"
last=$(tail -1 "$LOG")
check_has "19 log satirinda kayip_ankorlar bos" "$last" "\"kayip_ankorlar\": []"

out=$(printf '' | COMPACT_RESUME_PATH="$RESUME_OK" COMPACT_HISTORY_LOG="$LOG" python3 scripts/compact-postcheck.py)
r=$?
check "20 bos stdin cokmuyor" "$r" 0
check_not_has "21 bos ozette kanarya uyarisi YOK (gurultu yok)" "$out" "kanarya"

echo "=================================="
if [ "$fail" -eq 0 ]; then echo "TÜMÜ YEŞİL"; else echo "KIRMIZI VAR"; fi
exit "$fail"
