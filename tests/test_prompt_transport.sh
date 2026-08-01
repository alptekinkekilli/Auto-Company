#!/usr/bin/env bash
# Regression tests for prompt TRANSPORT (2026-08-01, cycles #7/#8 rc=126).
#
#   bash tests/test_prompt_transport.sh scripts/core/auto-loop.sh
#
# The bug class: the assembled cycle prompt (PROMPT.md + guardrails + consensus.md)
# was passed to every engine as ONE argv argument. Linux caps a single argument at
# MAX_ARG_STRLEN = 131072 bytes — independent of ARG_MAX — so the moment consensus
# growth pushed the total past the cap, exec failed E2BIG and bash reported rc=126
# on BOTH engines in the same iteration. rc=126 reads like "binary not executable";
# nothing pointed at the prompt.
#
# Contract pinned here:
#   1. claude CLI receives the prompt on STDIN — argv carries no prompt text.
#   2. codex CLI receives the prompt on STDIN via the documented `-` sentinel.
#   3. run_jcode_cycle refuses (named reason, no spawn) a prompt >= 126000 bytes.
#   4. run_jcode_cycle still passes a normal-size prompt as the `run` argv argument.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '${2:0:400}'"; fail=1 ;; esac; }
not_contains() { case "$2" in *"$3"*) echo "  FAIL $1: unexpected '$3'"; fail=1 ;; *) echo "  PASS $1" ;; esac; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# Stub engine binary: records argv (one line per arg) and stdin, echoes nothing.
STUB="$WORK/stub-engine"
printf '%s\n' '#!/usr/bin/env bash' \
    'printf "%s\n" "$@" > "$STUB_ARGV_FILE"' \
    'cat > "$STUB_STDIN_FILE"' \
    'exit 0' > "$STUB"
chmod +x "$STUB"

BIG_PROMPT=$(printf 'x%.0s' $(seq 1 1000))
BIG_PROMPT="PROMPT-MARKER-$BIG_PROMPT"

run_claude_stub() {
    STUB_ARGV_FILE="$WORK/argv" STUB_STDIN_FILE="$WORK/stdin" bash -c '
        set -uo pipefail
        PROJECT_DIR="'"$WORK"'"; RESOLVED_ENGINE_BIN="'"$STUB"'"
        MODEL="claude-sonnet-5"; CLAUDE_EFFORT="high"; CLAUDE_PERMISSION_MODE=""
        CYCLE_TIMEOUT_ACTIVE=5; CYCLE_TIMED_OUT=0; CURRENT_ENGINE_PID=""
        log() { :; }; _kill_engine_group() { :; }; _reap_watchdog() { rm -f "$2"; }
        check_usage_limit() { return 1; }
        '"$(awk '/^run_claude_cycle_cli\(\)/,/^}/' "$SRC")"'
        run_claude_cycle_cli "$1"
    ' _ "$2"
}

run_codex_stub() {
    STUB_ARGV_FILE="$WORK/argv" STUB_STDIN_FILE="$WORK/stdin" bash -c '
        set -uo pipefail
        PROJECT_DIR="'"$WORK"'"; RESOLVED_ENGINE_BIN="'"$STUB"'"
        MODEL="gpt-5.6-sol"; CODEX_EFFORT="low"; CODEX_SANDBOX_MODE="danger-full-access"
        CYCLE_TIMEOUT_ACTIVE=5; CYCLE_TIMED_OUT=0; CURRENT_ENGINE_PID=""
        log() { :; }; _kill_engine_group() { :; }; _reap_watchdog() { rm -f "$2"; }
        '"$(awk '/^run_codex_cycle_cli\(\)/,/^}/' "$SRC")"'
        run_codex_cycle_cli "$1"
    ' _ "$2"
}

echo "--- 1: claude CLI — prompt on stdin, never argv ---"
rm -f "$WORK/argv" "$WORK/stdin"
run_claude_stub _ "$BIG_PROMPT"
argv=$(cat "$WORK/argv" 2>/dev/null || echo MISSING)
stdin=$(cat "$WORK/stdin" 2>/dev/null || echo MISSING)
contains     "stdin carries prompt"   "$stdin" "PROMPT-MARKER-"
not_contains "argv clean of prompt"   "$argv"  "PROMPT-MARKER-"
contains     "print flag present"     "$argv"  "-p"

echo "--- 2: codex CLI — '-' sentinel + prompt on stdin ---"
rm -f "$WORK/argv" "$WORK/stdin"
run_codex_stub _ "$BIG_PROMPT"
argv=$(cat "$WORK/argv" 2>/dev/null || echo MISSING)
stdin=$(cat "$WORK/stdin" 2>/dev/null || echo MISSING)
contains     "stdin carries prompt"   "$stdin" "PROMPT-MARKER-"
not_contains "argv clean of prompt"   "$argv"  "PROMPT-MARKER-"
contains     "dash sentinel present"  "$argv"  "-"

echo "--- 3: jcode — >=126000-byte prompt refused pre-spawn with a named reason ---"
HUGE=$(printf 'y%.0s' $(seq 1 126001))
out=$(bash -c '
    set -uo pipefail
    PROJECT_DIR="'"$WORK"'"; JCODE_BIN="'"$STUB"'"
    MODEL="claude-sonnet-5"; CLAUDE_EFFORT="high"; CODEX_EFFORT="low"
    JCODE_TOOLS_ALLOW=""; JCODE_TOOLS_DENY=""
    CYCLE_TIMEOUT_ACTIVE=5; CYCLE_TIMED_OUT=0; CURRENT_ENGINE_PID=""
    STUB_ARGV_FILE="'"$WORK"'/argv3"; STUB_STDIN_FILE="'"$WORK"'/stdin3"
    export STUB_ARGV_FILE STUB_STDIN_FILE
    log() { echo "LOG:$*"; }; _kill_engine_group() { :; }; _reap_watchdog() { rm -f "$2"; }
    '"$(awk '/^run_jcode_cycle\(\)/,/^}/' "$SRC")"'
    run_jcode_cycle "$1" claude
    echo "EXIT_CODE=$EXIT_CODE OUTPUT=$OUTPUT"
' _ "$HUGE" 2>&1)
contains "named refusal logged"  "$out" "PROMPT-TOO-LARGE"
contains "cycle failed rc=1"     "$out" "EXIT_CODE=1"
[ ! -f "$WORK/argv3" ] && echo "  PASS engine never spawned" || { echo "  FAIL engine was spawned"; fail=1; }

echo "--- 4: jcode — normal prompt still travels as the run argv argument ---"
out=$(bash -c '
    set -uo pipefail
    PROJECT_DIR="'"$WORK"'"; JCODE_BIN="'"$STUB"'"
    MODEL="claude-sonnet-5"; CLAUDE_EFFORT="high"; CODEX_EFFORT="low"
    JCODE_TOOLS_ALLOW=""; JCODE_TOOLS_DENY=""
    CYCLE_TIMEOUT_ACTIVE=5; CYCLE_TIMED_OUT=0; CURRENT_ENGINE_PID=""
    STUB_ARGV_FILE="'"$WORK"'/argv4"; STUB_STDIN_FILE="'"$WORK"'/stdin4"
    export STUB_ARGV_FILE STUB_STDIN_FILE CLAUDE_CODE_OAUTH_TOKEN=""
    log() { echo "LOG:$*"; }; _kill_engine_group() { :; }; _reap_watchdog() { rm -f "$2"; }
    '"$(awk '/^run_jcode_cycle\(\)/,/^}/' "$SRC")"'
    run_jcode_cycle "$1" claude
    echo "EXIT_CODE=$EXIT_CODE"
' _ "$BIG_PROMPT" 2>&1)
argv4=$(cat "$WORK/argv4" 2>/dev/null || echo MISSING)
contains "argv carries prompt"     "$argv4" "PROMPT-MARKER-"
contains "run subcommand present"  "$argv4" "run"
contains "cycle completed rc=0"    "$out"   "EXIT_CODE=0"

echo
if [ "$fail" = "0" ]; then echo "ALL PASS"; else echo "FAILURES"; exit 1; fi
