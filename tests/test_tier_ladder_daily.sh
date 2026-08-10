#!/usr/bin/env bash
# apply_tier_ladder()'ın 5h/codex-cycle-count temelinden GÜNLÜK gerçek maliyet
# temeline geçişini doğrular (APP-263 follow-up, 2026-08-10 operatör kararı).
# Önceden hiç test edilmemiş bir fonksiyondu (_tier_pick'in kendi matematiği de
# dahil) — bu dosya ilk kapsamı sağlıyor.
#
#   bash tests/test_tier_ladder_daily.sh scripts/core/auto-loop.sh
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }
check_contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT

extract() { awk "/^$1\(\) \{/,/^\}/" "$SRC"; }
HARNESS="$SB/harness.sh"
{
    echo 'set -uo pipefail'
    echo 'log() { echo "$@"; }'
    echo 'ROUTER_TIER_LADDER="${ROUTER_TIER_LADDER:-1}"'
    echo 'CLAUDE_TIER_LADDER="${CLAUDE_TIER_LADDER:-claude-haiku-4-5,claude-sonnet-5,claude-opus-5}"'
    echo 'CODEX_TIER_LADDER="${CODEX_TIER_LADDER:-low,medium,high}"'
    echo 'TOTAL_DAILY_BUDGET_USD="${TOTAL_DAILY_BUDGET_USD:-}"'
    echo 'BG_CLAUDE_DAILY="${BG_CLAUDE_DAILY:-}"; BG_CODEX_DAILY="${BG_CODEX_DAILY:-}"'
    echo 'BASE_MODEL="claude-base"; BASE_CLAUDE_EFFORT="base-effort"; BASE_CODEX_EFFORT="base-codex-effort"'
    echo 'MODEL="$BASE_MODEL"; CLAUDE_EFFORT="$BASE_CLAUDE_EFFORT"; CODEX_EFFORT="$BASE_CODEX_EFFORT"'
    echo 'MODEL_LABEL=""; CODEX_MODEL="codex-base"; ENGINE="${ENGINE:-claude}"; CYCLE_ENGINE_OVERRIDE="${CYCLE_ENGINE_OVERRIDE:-}"'
    extract apply_tier_ladder
} > "$HARNESS"

run() { bash -c "source '$HARNESS'; $1" 2>&1; }

echo "--- 1: ladder OFF restores base config regardless of daily fill ---"
out="$(run 'ROUTER_TIER_LADDER=0 BG_CLAUDE_DAILY=499 TOTAL_DAILY_BUDGET_USD=500 apply_tier_ladder; echo "model=$MODEL effort=$CLAUDE_EFFORT"')"
check "off keeps base model" "$(echo "$out" | grep -o 'model=[^ ]*')" "model=claude-base"

echo "--- 2: TOTAL_DAILY_BUDGET_USD unset -> no fill signal -> cheapest tier (conservative) ---"
out="$(run 'BG_CLAUDE_DAILY=0 TOTAL_DAILY_BUDGET_USD= apply_tier_ladder; echo "model=$MODEL codex=$CODEX_EFFORT"')"
check "claude cheapest, no cap"  "$(echo "$out" | grep -o 'model=[^ ]*')" "model=claude-haiku-4-5"
check "codex cheapest, no cap"   "$(echo "$out" | grep -o 'codex=[^ ]*')" "codex=low"

echo "--- 3: Claude spent \$0 of \$500 today -> best tier ---"
out="$(run 'BG_CLAUDE_DAILY=0 TOTAL_DAILY_BUDGET_USD=500 apply_tier_ladder; echo "model=$MODEL"')"
check "claude best tier at 0% fill" "$(echo "$out" | grep -o 'model=[^ ]*')" "model=claude-opus-5"

echo "--- 4: Claude spent \$500 of \$500 today (100% fill) -> cheapest tier ---"
out="$(run 'BG_CLAUDE_DAILY=500 TOTAL_DAILY_BUDGET_USD=500 apply_tier_ladder; echo "model=$MODEL"')"
check "claude cheapest tier at 100% fill" "$(echo "$out" | grep -o 'model=[^ ]*')" "model=claude-haiku-4-5"

echo "--- 5: independent engines -- Claude idle, Codex near the shared daily cap ---"
# Bu, operatörün 2026-08-10 kararının çekirdeği: PAYLAŞILAN günlük cüzdana karşı
# ölçülen iki BAĞIMSIZ gerçek maliyet zinciri -- bir motorun harcaması kendi başına
# diğerinin katmanını düşürmemeli.
out="$(run 'BG_CLAUDE_DAILY=0 BG_CODEX_DAILY=450 TOTAL_DAILY_BUDGET_USD=500 apply_tier_ladder; echo "model=$MODEL codex=$CODEX_EFFORT"')"
check "claude unaffected by codex spend" "$(echo "$out" | grep -o 'model=[^ ]*')" "model=claude-opus-5"
check "codex downgraded by its own spend" "$(echo "$out" | grep -o 'codex=[^ ]*')" "codex=low"

echo "--- 6: reverse -- Codex idle, Claude near the shared daily cap ---"
out="$(run 'BG_CLAUDE_DAILY=480 BG_CODEX_DAILY=0 TOTAL_DAILY_BUDGET_USD=500 apply_tier_ladder; echo "model=$MODEL codex=$CODEX_EFFORT"')"
check "claude downgraded by its own spend" "$(echo "$out" | grep -o 'model=[^ ]*')" "model=claude-haiku-4-5"
check "codex unaffected by claude spend"   "$(echo "$out" | grep -o 'codex=[^ ]*')" "codex=high"

echo "--- 7: mid-fill (60% of \$500 = \$300) lands on the middle rung ---"
out="$(run 'BG_CLAUDE_DAILY=300 TOTAL_DAILY_BUDGET_USD=500 apply_tier_ladder; echo "model=$MODEL"')"
check "mid fill -> middle tier" "$(echo "$out" | grep -o 'model=[^ ]*')" "model=claude-sonnet-5"

echo "--- 8: [TIER] log line names 'daily' and 'today', not 5h/window ---"
out="$(run 'BG_CLAUDE_DAILY=10 BG_CODEX_DAILY=5 TOTAL_DAILY_BUDGET_USD=500 apply_tier_ladder')"
check_contains "log says daily"       "$out" "[TIER] fill-weighted (daily)"
check_contains "log shows claude today" "$out" "claude today \$10"
check_contains "log shows codex today"  "$out" "codex today \$5"
check_contains "no 5h wording"        "$out" "today"
case "$out" in
    *"5h"*) echo "  FAIL log still mentions 5h: $out"; fail=1 ;;
    *)      echo "  PASS log has no 5h wording" ;;
esac

echo "--- 9: MODEL_LABEL still reflects a Codex-routed cycle correctly ---"
out="$(run 'BG_CLAUDE_DAILY=0 TOTAL_DAILY_BUDGET_USD=500 CYCLE_ENGINE_OVERRIDE=codex apply_tier_ladder; echo "label=$MODEL_LABEL"')"
check_contains "label shows codex, not claude" "$out" "label=codex-base:"

if [ "$fail" -eq 0 ]; then
    echo "ALL PASS"
    exit 0
else
    echo "SOME FAILED"
    exit 1
fi
