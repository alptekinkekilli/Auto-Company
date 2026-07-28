#!/usr/bin/env bash
# Regression tests for auto-loop.sh's one-shot operator escalation (APP-238).
#
#   bash tests/test_escalation.sh scripts/core/auto-loop.sh
#
# Sources ONLY the functions under test into a throwaway PROJECT_DIR so no live
# runtime.env / human-directive.md is touched. The invariant that matters: an
# escalation is consumed exactly once, and a refusal leaves it ARMED rather than
# silently burning an approval the operator deliberately gave.
# Exercises apply_cycle_escalation() in isolation by sourcing only the functions
# it needs, against a throwaway runtime.env + human-directive.md.
set -uo pipefail
SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT
mkdir -p "$SB/logs" "$SB/memories" "$SB/scripts/core"
PROJECT_DIR="$SB"; LOG_DIR="$SB/logs"; SCRIPT_DIR="$SB/scripts/core"
CYCLE_TIMEOUT_SECONDS=900; ESCALATED_CYCLE_TIMEOUT_SECONDS=1800
CYCLE_TIMEOUT_ACTIVE="$CYCLE_TIMEOUT_SECONDS"
ENGINE=claude; CYCLE_ENGINE_OVERRIDE=""; MODEL="ladder-model"; CLAUDE_EFFORT="low"; MODEL_LABEL="$MODEL"
TELEGRAM_BOT_TOKEN=""; TELEGRAM_CHAT_ID=""
log() { echo "LOG: $*"; }

# pull the three functions under test out of the real script
SRC="$1"
eval "$(awk '/^_read_runtime_env_key\(\)/,/^}/' "$SRC")"
eval "$(awk '/^_consume_escalation\(\)/,/^}/' "$SRC")"
eval "$(awk '/^_directive_is_pending\(\)/,/^}/' "$SRC")"
eval "$(awk '/^apply_cycle_escalation\(\)/,/^}$/' "$SRC")"

arm()      { printf 'FOO=bar\nESCALATE_NEXT_CYCLE=%s\nBAZ=qux\n' "$1" > "$LOG_DIR/runtime.env"; }
directive(){ printf '# Human Directive\n\n## Status\n%s\n\n## Directive\nx\n' "$1" > "$PROJECT_DIR/memories/human-directive.md"; }
armed()    { grep -q '^ESCALATE_NEXT_CYCLE=' "$LOG_DIR/runtime.env" && echo ARMED || echo CLEARED; }
reset()    { MODEL="ladder-model"; CLAUDE_EFFORT="low"; CYCLE_ENGINE_OVERRIDE=""; }
fail=0
check()   { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }

echo "--- 1: PENDING directive + claude cycle -> consumed, model overridden, long wall ---"
reset; arm "claude-opus-5:high"; directive PENDING; apply_cycle_escalation
check "model"    "$MODEL" "claude-opus-5"
check "effort"   "$CLAUDE_EFFORT" "high"
check "wall"     "$CYCLE_TIMEOUT_ACTIVE" "1800"
check "consumed" "$(armed)" "CLEARED"
echo "  runtime.env now:"; sed 's/^/    /' "$LOG_DIR/runtime.env"
check "other keys kept" "$(grep -cE '^(FOO=bar|BAZ=qux)$' "$LOG_DIR/runtime.env")" "2"

echo "--- 2: directive DONE -> refused, stays armed, ladder pick untouched ---"
reset; arm "claude-opus-5:high"; directive DONE; apply_cycle_escalation
check "model untouched" "$MODEL" "ladder-model"
check "wall default"    "$CYCLE_TIMEOUT_ACTIVE" "900"
check "still armed"     "$(armed)" "ARMED"

echo "--- 3: routed to Codex -> refused, stays armed ---"
reset; arm "claude-opus-5:high"; directive PENDING; CYCLE_ENGINE_OVERRIDE="codex"; apply_cycle_escalation
check "model untouched" "$MODEL" "ladder-model"
check "still armed"     "$(armed)" "ARMED"

echo "--- 4: nothing armed -> no-op, default wall ---"
reset; printf 'FOO=bar\n' > "$LOG_DIR/runtime.env"; directive PENDING; apply_cycle_escalation
check "model untouched" "$MODEL" "ladder-model"
check "wall default"    "$CYCLE_TIMEOUT_ACTIVE" "900"

echo "--- 5: cannot fire twice (re-run immediately after a consume) ---"
reset; arm "claude-opus-5:high"; directive PENDING; apply_cycle_escalation >/dev/null
reset; apply_cycle_escalation
check "second run no-op" "$MODEL" "ladder-model"
check "wall back to default" "$CYCLE_TIMEOUT_ACTIVE" "900"

echo; [ "$fail" = 0 ] && echo "ALL PASS" || { echo "FAILURES"; exit 1; }
