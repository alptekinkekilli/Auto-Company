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
# 3 turns / 40s / 146 messages: under the old bars this was BLOATED purely on message
# count. It is a short, cheap, fast session — the recalibration must call it ok, and this
# assertion is the one that proves msgs_max no longer votes.
contains "high msgs alone is ok" "$out" "verdict=ok"

echo "--- 3: threshold BOUNDARIES are pinned (recalibrated 2026-08-02 from 34 cycles) ---"
# The old 40-turn / 80-message bars fired on 14 of 34 real cycles (41%) — an alarm at that
# rate is noise, and msgs_max was never independent (it tracks turns at ~2x). The bars now
# sit at the measured p80/p90 and add the two facts that actually hurt: nearing the 900s
# watchdog, and cost. These cases fail loudly if anyone moves them without new evidence.
BOUND="$WORK/jcode-2026-08-02.log"
# NOTE: session names must match session_<letters>_<digits> or the parser skips
# them entirely and every assertion fails as 'no sessions found'.
mk_session() { # $1 session  $2 turns  $3 msgs_per_turn  [$4 seconds between turns]
    step="${4:-0}"
    for i in $(seq 1 "$2"); do
        secs=$(( i * step ))
        mk_t=$(printf '%02d:%02d:%02d' $(( 3 + secs / 3600 )) $(( (secs % 3600) / 60 )) $(( secs % 60 )))
        mkline "$mk_t" "$1" "API call starting: $(( i * $3 )) messages, 129 tools"
    done
}
: > "$BOUND"
mk_session session_boundary_1 56 1 >> "$BOUND"   # 56 turns -> CHATTY
out=$(python3 "$AUDIT" "$BOUND" --summary-last)
contains "56 turns is CHATTY"   "$out" "verdict=CHATTY"
: > "$BOUND"
mk_session session_boundary_2 55 1 >> "$BOUND"   # exactly at the bar -> still ok
out=$(python3 "$AUDIT" "$BOUND" --summary-last)
contains "55 turns still ok"    "$out" "verdict=ok"
: > "$BOUND"
mk_session session_boundary_3 66 1 >> "$BOUND"   # past p90 -> BLOATED
out=$(python3 "$AUDIT" "$BOUND" --summary-last)
contains "66 turns is BLOATED"  "$out" "verdict=BLOATED"
: > "$BOUND"
# The regression that started this: 40 turns / 81 messages / 298s / $2.38 was flagged
# BLOATED and was in fact a perfectly healthy cycle. It must now read ok.
mk_session session_boundary_4 40 2 >> "$BOUND"   # 40 turns, msgs_max 80
out=$(python3 "$AUDIT" "$BOUND" --summary-last)
contains "40t/80m now ok"       "$out" "verdict=ok"
: > "$BOUND"
# Duration alone must be able to raise BLOATED: a short-turn cycle can still crawl toward
# the watchdog, and that is the failure that loses tail work.
mk_session session_boundary_5 20 1 40 >> "$BOUND"   # 20 turns spread over 800s
out=$(python3 "$AUDIT" "$BOUND" --summary-last)
contains "long-but-quiet BLOATED" "$out" "verdict=BLOATED"

echo "--- 4: verdict=ok for the small session (via full report) ---"
out=$(python3 "$AUDIT" "$LOG" | grep session_ant_1000)
contains "ok verdict" "$out" "verdict=ok"

echo
if [ "$fail" = "0" ]; then echo "ALL PASS"; else echo "FAILURES"; exit 1; fi
