#!/usr/bin/env bash
# Regression tests for scripts/ops/turn-audit.py (turn-economy policy, sec. 4).
#
#   bash tests/test_turn_audit.sh
#
# Pins: session parsing from jcode daily-log lines, turn/message counting, cache
# accounting, --summary-last picking the NEWEST session, and the CHATTY/BLOATED
# verdict thresholds.
set -uo pipefail
AUDIT="${1:-scripts/ops/turn-audit.py}"
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '${2:0:300}'"; fail=1 ;; esac; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
LOG="$WORK/jcode-2026-08-01.log"

mkline() { # $1 time $2 session $3 rest
    printf '[2026-08-01 %s.000] [INFO] [ses:%s|prv:Claude|mod:claude-sonnet-5] %s\n' "$1" "$2" "$3"
}

{
    # old small session: 2 turns
    mkline 01:00:00 session_ant_1000 'API call starting: 2 messages, 129 tools'
    mkline 01:00:05 session_ant_1000 'EVENT event=AGENT_PROVIDER_STREAM_LIFECYCLE cache_read=1000 cache_write=500 connection_type=https/sse elapsed_ms=100'
    mkline 01:00:06 session_ant_1000 'Tool finished: bash in 1.00s'
    mkline 01:00:10 session_ant_1000 'API call starting: 4 messages, 129 tools'
    # newest session: 3 turns, bloated context
    mkline 02:00:00 session_yak_2000 'API call starting: 2 messages, 129 tools'
    mkline 02:00:10 session_yak_2000 'EVENT event=AGENT_PROVIDER_STREAM_LIFECYCLE cache_read=200000 cache_write=130000 connection_type=https/sse elapsed_ms=100'
    mkline 02:00:20 session_yak_2000 'API call starting: 80 messages, 129 tools'
    mkline 02:00:30 session_yak_2000 'EVENT event=AGENT_PROVIDER_STREAM_LIFECYCLE cache_read=250000 cache_write=1000 connection_type=https/sse elapsed_ms=100'
    mkline 02:00:35 session_yak_2000 'Tool finished: webfetch in 2.50s'
    mkline 02:00:40 session_yak_2000 'API call starting: 146 messages, 129 tools'
} > "$LOG"

echo "--- 1: full report parses both sessions ---"
out=$(python3 "$AUDIT" "$LOG")
contains "old session present"   "$out" "session_ant_1000"
contains "new session present"   "$out" "session_yak_2000"
contains "old turn count"        "$out" "turns=2"
contains "tool census"           "$out" "bash"

echo "--- 2: --summary-last picks the NEWEST session only ---"
out=$(python3 "$AUDIT" "$LOG" --summary-last)
contains "newest chosen"     "$out" "session_yak_2000"
case "$out" in *session_ant_1000*) echo "  FAIL old session leaked"; fail=1 ;; *) echo "  PASS old session excluded" ;; esac
contains "turns counted"     "$out" "turns=3"
contains "msgs tracked"      "$out" "msgs_max=146"
contains "cache summed"      "$out" "cache_read=450000"
contains "BLOATED verdict"   "$out" "verdict=BLOATED"

echo "--- 3: verdict=ok for the small session (via full report) ---"
out=$(python3 "$AUDIT" "$LOG" | grep session_ant_1000)
contains "ok verdict" "$out" "verdict=ok"

echo
if [ "$fail" = "0" ]; then echo "ALL PASS"; else echo "FAILURES"; exit 1; fi
