#!/usr/bin/env bash
# APP-263 follow-up (2026-08-10 operator decision): apply_tier_ladder()'s fill signal
# moved from the retired 5h-window/codex-cycle-count basis to each engine's OWN real
# spend TODAY against the shared TOTAL_DAILY_BUDGET_USD ceiling (BG_CLAUDE_DAILY /
# BG_CODEX_DAILY, populated by evaluate_budget_gates() in the real per-cycle sequence —
# here set directly, since apply_tier_ladder() only READS them).
#
#   bash tests/test_tier_ladder_daily.sh scripts/core/auto-loop.sh
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT

extract() { awk "/^$1\(\) \{/,/^\}/" "$SRC"; }
HARNESS="$SB/harness.sh"
{
    echo 'set -uo pipefail'
    echo 'log() { echo "$@" >&2; }'
    echo 'BASE_MODEL="claude-base"; BASE_CLAUDE_EFFORT="base-effort"; BASE_CODEX_EFFORT="base-codex-effort"'
    echo 'MODEL="$BASE_MODEL"; CLAUDE_EFFORT="$BASE_CLAUDE_EFFORT"; CODEX_EFFORT="$BASE_CODEX_EFFORT"'
    echo 'CODEX_MODEL="codex-model"; ENGINE="claude"; CYCLE_ENGINE_OVERRIDE=""; MODEL_LABEL=""'
    echo 'ROUTER_TIER_LADDER="${ROUTER_TIER_LADDER:-1}"'
    echo 'CLAUDE_TIER_LADDER="${CLAUDE_TIER_LADDER:-cheap,mid,best}"'
    echo 'CODEX_TIER_LADDER="${CODEX_TIER_LADDER:-xcheap,xmid,xbest}"'
    echo 'TOTAL_DAILY_BUDGET_USD="${TOTAL_DAILY_BUDGET_USD:-}"'
    echo 'BG_CLAUDE_DAILY="${BG_CLAUDE_DAILY:-0}"; BG_CODEX_DAILY="${BG_CODEX_DAILY:-0}"'
    extract "apply_tier_ladder"
} > "$HARNESS"

run() { bash -c "source '$HARNESS'; $1" 2>/dev/null; }

echo "== test_tier_ladder_daily =="

echo "--- 1: ladder OFF restores base config, ignores BG_* entirely ---"
out="$(run 'ROUTER_TIER_LADDER=0 TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=499 apply_tier_ladder; echo "MODEL=$MODEL EFFORT=$CLAUDE_EFFORT"')"
check "off: restores BASE_MODEL"         "$out" "MODEL=claude-base EFFORT=base-effort"

echo "--- 2: TOTAL_DAILY_BUDGET_USD unset -> no fill signal -> cheapest tier (both engines) ---"
out="$(run 'TOTAL_DAILY_BUDGET_USD= BG_CLAUDE_DAILY=0 BG_CODEX_DAILY=0 apply_tier_ladder; echo "MODEL=$MODEL CODEX_EFFORT=$CODEX_EFFORT"')"
check "no cap: claude cheapest"          "$out" "MODEL=cheap CODEX_EFFORT=xcheap"

echo "--- 3: day empty (0 spent of \$500) -> most capable tier ---"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=0 BG_CODEX_DAILY=0 apply_tier_ladder; echo "MODEL=$MODEL CODEX_EFFORT=$CODEX_EFFORT"')"
check "empty day: claude best"           "$out" "MODEL=best CODEX_EFFORT=xbest"

echo "--- 4: day full (\$500 of \$500) -> cheapest tier ---"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=500 BG_CODEX_DAILY=500 apply_tier_ladder; echo "MODEL=$MODEL CODEX_EFFORT=$CODEX_EFFORT"')"
check "full day: claude cheapest"        "$out" "MODEL=cheap CODEX_EFFORT=xcheap"

echo "--- 5: mid-fill (\$250 of \$500, 3-rung ladder) -> middle tier ---"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=250 BG_CODEX_DAILY=250 apply_tier_ladder; echo "MODEL=$MODEL CODEX_EFFORT=$CODEX_EFFORT"')"
check "mid fill: claude mid"             "$out" "MODEL=mid CODEX_EFFORT=xmid"

echo "--- 6: THE key new behavior -- one engine's spend does not move the other's tier ---"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=500 BG_CODEX_DAILY=0 apply_tier_ladder; echo "MODEL=$MODEL CODEX_EFFORT=$CODEX_EFFORT"')"
check "claude full + codex empty: claude cheapest, codex best"  "$out" "MODEL=cheap CODEX_EFFORT=xbest"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=0 BG_CODEX_DAILY=500 apply_tier_ladder; echo "MODEL=$MODEL CODEX_EFFORT=$CODEX_EFFORT"')"
check "claude empty + codex full: claude best, codex cheapest"  "$out" "MODEL=best CODEX_EFFORT=xcheap"

echo "--- 7: MODEL_LABEL on a Codex-routed cycle still shows codex model:effort (unchanged behavior) ---"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=0 BG_CODEX_DAILY=500 CYCLE_ENGINE_OVERRIDE=codex apply_tier_ladder; echo "LABEL=$MODEL_LABEL"')"
check "codex cycle: label shows codex-model:effort" "$out" "LABEL=codex-model:xcheap"

echo "--- 8: model:effort rung syntax (single ladder entry combining both) still works ---"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 BG_CLAUDE_DAILY=0 CLAUDE_TIER_LADDER="claude-sonnet-5:low,claude-opus-5:high" apply_tier_ladder; echo "MODEL=$MODEL EFFORT=$CLAUDE_EFFORT"')"
check "combined rung: best tier picks opus:high" "$out" "MODEL=claude-opus-5 EFFORT=high"

echo
if [ "$fail" = "0" ]; then
  echo "ALL PASS"
else
  echo "SOME FAILED"
fi
exit "$fail"
