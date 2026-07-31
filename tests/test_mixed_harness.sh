#!/usr/bin/env bash
# Regression tests for the MIXED harness configuration (claude→jcode, codex→cli).
#
#   bash tests/test_mixed_harness.sh scripts/core/auto-loop.sh
#
# The bug class this exists for: under a mixed boot, no single global describes a
# cycle. LOOP_HARNESS says "jcode" while a codex-routed cycle in the same loop
# iteration ran on the CLI — so any code that reads the GLOBAL to decide how to parse
# a result, what to charge, or how to label a ledger row will do the wrong thing to
# every other cycle. It fails silently: the loop keeps running, the numbers are wrong.
#
# Each case drives extract_cycle_metadata() with the actual-cycle variables the
# dispatchers set, under the same `set -euo pipefail` production uses.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }

# One cycle through the metadata extractor.
#   $1 harness_used  $2 provider_used  $3 ENGINE  $4 override  $5 fallback
#   $6 result_message  $7 jcode_cost_json  $8 exit_code
run_cycle() {
    bash -c '
        set -euo pipefail
        CYCLE_HARNESS_USED="$1"; CYCLE_PROVIDER_USED="$2"
        ENGINE="$3"; CYCLE_ENGINE_OVERRIDE="$4"; FALLBACK_USED="$5"
        RESULT_MESSAGE="$6"; JCODE_COST_JSON="$7"; EXIT_CODE="$8"
        OUTPUT="raw stderr tail"; CYCLE_COST="N/A"
        log() { echo "LOG:$*"; }
        latch_budget_hold() { echo "LATCH:$*"; }
        '"$(awk '/^_cycle_ran_on_codex\(\)/,/^}/' "$SRC")"'
        '"$(awk '/^extract_cycle_metadata\(\)/,/^}/' "$SRC")"'
        extract_cycle_metadata
        printf "type=%s subtype=%s cost=%s rc=%s text=%s" \
            "$CYCLE_TYPE" "$CYCLE_SUBTYPE" "$CYCLE_COST" "$EXIT_CODE" "${RESULT_TEXT:0:24}"
    ' _ "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" 2>&1
    echo "|shell_rc=$?"
}

JCODE_COST='{"model":"claude-sonnet-5","cost_usd":0.42,"estimated":false}'
CODEX_MSG='Cycle complete. Reviewed the tender packet.'
CLAUDE_CLI_MSG='Ignoring 3 permissions.allow entries
{"type":"result","subtype":"success","total_cost_usd":1.23,"result":"did the thing"}'

echo "--- 1: Codex-CLI is the FIRST cycle of a mixed boot (no jcode cycle before it) ---"
# The jcode branch must not claim this cycle just because LOOP_HARNESS=jcode globally.
out=$(run_cycle cli openai codex "" 0 "$CODEX_MSG" "" 0)
contains "survives"            "$out" "shell_rc=0"
contains "typed as codex_exec" "$out" "type=codex_exec"
contains "no jcode cost"       "$out" "cost=N/A"

echo "--- 2: Claude-jcode, then Codex-CLI (stale cost must not carry over) ---"
out=$(run_cycle jcode claude claude "" 0 "SUMMARY: jcode did it" "$JCODE_COST" 0)
contains "jcode cycle charged"  "$out" "cost=0.42"
contains "typed jcode_claude"   "$out" "type=jcode_claude"
# the next cycle is CLI-codex; run_engine_cycle clears JCODE_COST_JSON, so it arrives empty
out=$(run_cycle cli openai claude codex 0 "$CODEX_MSG" "" 0)
contains "cli cycle not charged jcode cost" "$out" "cost=N/A"
contains "cli cycle typed codex_exec"       "$out" "type=codex_exec"

echo "--- 3: Codex-CLI, then Claude-jcode ---"
out=$(run_cycle cli openai claude codex 0 "$CODEX_MSG" "" 0)
contains "cli first survives" "$out" "shell_rc=0"
out=$(run_cycle jcode claude claude "" 0 "SUMMARY: back on jcode" "$JCODE_COST" 0)
contains "jcode second charged" "$out" "cost=0.42"
contains "jcode second labelled" "$out" "type=jcode_claude"

echo "--- 4: usage-limit FALLBACK — claude(jcode) limited, retried on codex(CLI) ---"
# FALLBACK_USED=1 is assigned AFTER the engine call returns, so the metadata pass sees
# the codex cycle with the CLI harness. It must parse as CLI prose, not as jcode.
out=$(run_cycle cli openai claude "" 1 "$CODEX_MSG" "" 0)
contains "fallback survives"        "$out" "shell_rc=0"
contains "fallback typed codex"     "$out" "type=codex_exec"
contains "fallback not jcode-costed" "$out" "cost=N/A"

echo "--- 5: budget OVERRIDE route (claude gate closed -> codex CLI) ---"
out=$(run_cycle cli openai claude codex 0 "$CODEX_MSG" "" 0)
contains "override survives"    "$out" "shell_rc=0"
contains "override typed codex" "$out" "type=codex_exec"

echo "--- 6: a jcode cycle with NO cost number must FAIL AND LATCH (REVISE-2 A4) ---"
out=$(run_cycle jcode claude claude "" 0 "SUMMARY: ran but unmetered" "" 0)
contains "marked error"      "$out" "subtype=error"
contains "exit code raised"  "$out" "rc=1"
contains "latched immediately" "$out" "LATCH:"

echo "--- 7: a jcode cycle whose adapter returned JSON without cost_usd also fails+latches ---"
out=$(run_cycle jcode claude claude "" 0 "SUMMARY: x" '{"model":"claude-sonnet-5","estimated":true}' 0)
contains "no-number marked error" "$out" "subtype=error"
contains "no-number raises rc"    "$out" "rc=1"
contains "no-number latches"      "$out" "LATCH:"

echo "--- 7b: a COMPLETED jcode cycle reporting \$0 is unmetered, not free — latches ---"
out=$(run_cycle jcode claude claude "" 0 "SUMMARY: y" '{"model":"claude-sonnet-5","cost_usd":0,"estimated":false}' 0)
contains "zero-cost marked error" "$out" "subtype=error"
contains "zero-cost raises rc"    "$out" "rc=1"
contains "zero-cost latches"      "$out" "LATCH:"

echo "--- 7c: a zero cost on an ALREADY-FAILED cycle is not double-reported ---"
out=$(run_cycle jcode claude claude "" 0 "" '{"model":"claude-sonnet-5","cost_usd":0,"estimated":false}' 124)
contains "timeout keeps its own rc" "$out" "rc=124"

echo "--- 8: CLI-claude on a mixed boot still parses its own JSON result ---"
out=$(run_cycle cli claude claude "" 0 "$CLAUDE_CLI_MSG" "" 0)
contains "cli claude cost parsed" "$out" "cost=1.23"
contains "cli claude typed"       "$out" "type=result"

# ── REVISE-2 gate A5: the Claude ATTEMPT is persisted BEFORE the Codex retry ──
# Drives run_engine_cycle with stubbed engines + a REAL record_total_spend and a
# real ledger file, so the assertion is on ledger ROWS, not on log lines.
#   $1 = harness the claude attempt ran on   $2 = attempt cost json / result msg
run_fallback() {
    local SB; SB="$(mktemp -d)"
    bash -c '
        set -euo pipefail
        SB="$1"; H="$2"; PAYLOAD="$3"
        TOTAL_SPEND_LEDGER="$SB/spend-total.log"; TOTAL_LEDGER_RETENTION_DAYS=90
        LOOP_BOOT_ID=fbtest; loop_count=7; LOG_DIR="$SB"
        ENGINE=claude; FALLBACK_ENGINE=codex; CYCLE_ENGINE_OVERRIDE=""
        RESOLVED_ENGINE_BIN=/bin/true; RESOLVED_CODEX_BIN=/bin/true
        MODEL=claude-sonnet-5; CODEX_MODEL=""; CLAUDE_5H_BUDGET_USD=100
        LOOP_HARNESS=cli; LOOP_HARNESS_CODEX=cli
        log() { echo "LOG:$*"; }
        latch_budget_hold() { echo "LATCH:$*"; }
        _budget_now() { date +%s; }
        window_spend() { echo 1.0; }
        check_usage_limit() { return 0; }   # always "limited" for this test
        resolve_codex_bin() { echo /bin/true; }
        run_claude_cycle() {
            CYCLE_PROVIDER_USED=claude; CYCLE_HARNESS_USED="$H"
            OUTPUT="usage limit reached"; EXIT_CODE=1
            if [ "$H" = jcode ]; then
                RESULT_MESSAGE="limited"; JCODE_COST_JSON="$PAYLOAD"
            else
                RESULT_MESSAGE="$PAYLOAD"; JCODE_COST_JSON=""
            fi
        }
        run_codex_cycle() {
            echo "CODEX_RAN jcode_cost_json_at_codex_start=[${JCODE_COST_JSON:-}]"
            CYCLE_PROVIDER_USED=openai; CYCLE_HARNESS_USED=cli
            OUTPUT="codex output"; RESULT_MESSAGE="Cycle complete."; EXIT_CODE=0
        }
        '"$(awk '/^record_total_spend\(\)/,/^}/' "$SRC")"'
        '"$(awk '/^run_engine_cycle\(\)/,/^}/' "$SRC")"'
        run_engine_cycle "prompt"
        echo "FALLBACK_USED=$FALLBACK_USED"
        echo "LEDGER:$(cat "$SB/spend-total.log" 2>/dev/null | tr "\n" ";")"
    ' _ "$SB" "$@" 2>&1
    rm -rf "$SB"
}

echo "--- 9: jcode-claude attempt cost persisted under its own run ID before codex ---"
out=$(run_fallback jcode '{"model":"claude-sonnet-5","cost_usd":0.31,"estimated":false}')
contains "attempt row written"     "$out" "claude fbtest-c7-fb-claude 0.31"
contains "codex retry ran"         "$out" "CODEX_RAN"
contains "cost json cleared first" "$out" "jcode_cost_json_at_codex_start=[]"
contains "fallback flagged"        "$out" "FALLBACK_USED=1"

echo "--- 9b: CLI-claude attempt cost parsed from its result JSON and persisted ---"
out=$(run_fallback cli '{"type":"result","subtype":"error","total_cost_usd":0.0821,"result":"limit"}')
contains "cli attempt row written" "$out" "claude fbtest-c7-fb-claude 0.0821"
contains "cli codex retry ran"     "$out" "CODEX_RAN"

echo "--- 9c: \$0 attempt persists nothing but the retry still runs ---"
out=$(run_fallback cli '{"type":"result","subtype":"error","total_cost_usd":0,"result":"limit"}')
case "$out" in *"fb-claude"*) echo "  FAIL zero attempt wrote a row"; fail=1 ;; *) echo "  PASS no ledger row for \$0 attempt" ;; esac
contains "zero attempt: retry ran" "$out" "CODEX_RAN"

echo "--- 9d: UNPARSEABLE attempt cost LATCHES and blocks the codex retry ---"
out=$(run_fallback cli 'no json here at all')
contains "latched"                 "$out" "LATCH:claude fallback attempt spend unmeasurable"
case "$out" in *CODEX_RAN*) echo "  FAIL codex ran despite unmeasured claude spend"; fail=1 ;; *) echo "  PASS codex retry blocked" ;; esac
contains "no fallback flag"        "$out" "FALLBACK_USED=0"

echo
if [ "$fail" -eq 0 ]; then echo "ALL MIXED-HARNESS TESTS PASS"; else echo "FAILURES PRESENT"; exit 1; fi
