#!/usr/bin/env bash
# REVISE-2 gates A1/A2: ccusage measurement is fail-closed and a non-clean read
# can never lower a same-period prior observation.
#
#   bash tests/test_ccusage_failclosed.sh scripts/core/auto-loop.sh
#
# Same extraction harness as test_budget_gates.sh: functions pulled with awk,
# ccusage stubbed on PATH, clock pinned via BUDGET_NOW_OVERRIDE.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }
check_contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT
mkdir -p "$SB/bin"
NOW=1786017600
cat > "$SB/bin/ccusage" <<EOS
#!/usr/bin/env bash
[ -f "$SB/ccusage.json" ] || exit 1
cat "$SB/ccusage.json"
EOS
chmod +x "$SB/bin/ccusage"
iso() { python3 -c "import datetime,sys; print(datetime.datetime.fromtimestamp(int(sys.argv[1]), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'))" "$1"; }

extract() { awk "/^$1\(\) \{/,/^\}/" "$SRC"; }
HARNESS="$SB/harness.sh"
{
    echo 'set -uo pipefail'
    echo "LOG_DIR=\"$SB\"; WINDOW_SECONDS=18000; BUDGET_PAUSE_SECONDS=1800"
    echo "OPERATOR_USAGE_FILE=\"$SB/operator-usage.json\"; OPERATOR_USAGE_STALE_SECS=900"
    echo "TOTAL_SPEND_LEDGER=\"$SB/spend-total.log\"; TOTAL_LEDGER_RETENTION_DAYS=90"
    echo "ANALYST_SESSIONS_FILE=\"$SB/analyst.log\"; CODEX_SPEND_CACHE=\"$SB/.codex-spend-cache\""
    echo "CLAUDE_5H_BUDGET_USD=\"\${CLAUDE_5H_BUDGET_USD:-}\"; CODEX_5H_BUDGET_USD=\"\${CODEX_5H_BUDGET_USD:-}\""
    echo "TOTAL_DAILY_BUDGET_USD=\"\${TOTAL_DAILY_BUDGET_USD:-}\"; TOTAL_WEEKLY_BUDGET_USD=\"\${TOTAL_WEEKLY_BUDGET_USD:-}\""
    echo 'log() { echo "$@"; }'
    echo "LOOP_HOLD_FILE=\"$SB/LOOP_HOLD\""
    echo 'latch_budget_hold() { echo "LATCHED: $1" > "$LOOP_HOLD_FILE"; echo "LATCH:$1"; }'
    for f in _budget_now _utc_day_start _fmt_utc _window_anchor_epoch window_spend \
             record_total_spend claude_spend_since codex_ledger_spend_since _max_usd _sum_usd \
             _codex_spend_since _codex_spend_entries_since _weekly_resume_epoch \
             evaluate_budget_gates; do
        extract "$f"; echo ""
    done
} > "$HARNESS"

run() { PATH="$SB/bin:$PATH" BUDGET_NOW_OVERRIDE="$NOW" bash -c "source '$HARNESS'; $1" 2>&1; }
reset_state() { rm -f "$SB"/.codex-spend-cache-* "$SB"/ccusage.json "$SB"/LOOP_HOLD "$SB"/spend-total.log; }
one_session() { # $1 costUSD-json-fragment  $2 lastActivity-json-fragment
    printf '{"sessions":[{%s%s"sessionFile":"rollout-x"}]}' "$1" "$2" > "$SB/ccusage.json"
}
clean_50() { one_session '"costUSD": 50.0, ' "\"lastActivity\": \"$(iso $((NOW - 300)))\", "; }

echo "--- A1: first-ever ccusage failure with NO cache LATCHES, never a usable 0 ---"
reset_state
out="$(run 'evaluate_budget_gates; echo "ok_c=$BG_CLAUDE_OK ok_x=$BG_CODEX_OK gate=$BG_TOTAL_GATE"')"
check_contains "latch fired"     "$out" "LATCH:ccusage failed with no cached observation"
check_contains "gates closed"    "$out" "ok_c=0 ok_x=0"
check_contains "gate unreadable" "$out" "gate=UNREADABLE"
check "hold file written" "$([ -f "$SB/LOOP_HOLD" ] && echo yes)" "yes"
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "raw figure is NA, not 0" "$out" "NA 1"

echo "--- A2a: sessions:[] does not lower a same-period prior observation ---"
reset_state
clean_50
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null   # prime: clean 50
printf '{"sessions":[]}' > "$SB/ccusage.json"
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "kept 50, flagged stale" "$out" "50.0000 1"

echo "--- A2b: missing lastActivity (unplaceable session) does not lower it ---"
reset_state
clean_50
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null
one_session '"costUSD": 1.0, ' ""
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "kept 50, flagged stale" "$out" "50.0000 1"

echo "--- A2c: missing/invalid costUSD does not lower it ---"
reset_state
clean_50
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null
one_session '"costUSD": "not-a-number", ' "\"lastActivity\": \"$(iso $((NOW - 200)))\", "
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "kept 50, flagged stale" "$out" "50.0000 1"
one_session '' "\"lastActivity\": \"$(iso $((NOW - 200)))\", "
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "absent costUSD also kept 50" "$out" "50.0000 1"

echo "--- A2d: a degraded read HIGHER than the observation is taken (max) ---"
reset_state
clean_50
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null
printf '{"sessions":[{"costUSD": 80.0, "lastActivity": "%s", "sessionFile": "a"},{"costUSD": 1.0, "sessionFile": "b"}]}' "$(iso $((NOW - 200)))" > "$SB/ccusage.json"
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "took the higher figure" "$out" "80.0000 1"

echo "--- A2e: degraded reads never overwrite the cache (observation survives) ---"
reset_state
clean_50
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null
printf '{"sessions":[]}' > "$SB/ccusage.json"
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null   # stale read
clean_50
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "clean read restored, not poisoned" "$out" "50.0000 0"

echo "--- A2f: structurally invalid JSON is a FAILURE (stale path), not a \$0 ---"
reset_state
clean_50
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null
printf '{"totals": {"costUSD": 1}}' > "$SB/ccusage.json"      # no sessions list
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "kept 50, flagged stale" "$out" "50.0000 1"

echo "--- A1b: the three period refreshes fail INDEPENDENTLY ---"
reset_state
clean_50
run 'evaluate_budget_gates >/dev/null' >/dev/null              # primes 5h+daily+weekly caches
rm -f "$SB/.codex-spend-cache-daily"                           # daily observation lost
rm -f "$SB/ccusage.json"                                       # ccusage now fails
out="$(run 'evaluate_budget_gates; echo "ok_x=$BG_CODEX_OK"')"
check_contains "daily NA latches even though 5h+weekly have caches" "$out" "LATCH:ccusage failed with no cached observation"
check_contains "gates closed" "$out" "ok_x=0"

echo "--- A2g: a clean LOWER read stands (analyst exclusion is legitimate) ---"
reset_state
clean_50
run '_codex_spend_since '"$((NOW - 18000))"' 5h' >/dev/null
one_session '"costUSD": 2.0, ' "\"lastActivity\": \"$(iso $((NOW - 100)))\", "
out="$(run '_codex_spend_since '"$((NOW - 18000))"' 5h')"
check "clean lower accepted" "$out" "2.0000 0"

echo ""
[ "$fail" -eq 0 ] && echo "ALL CCUSAGE FAIL-CLOSED TESTS PASS" || { echo "FAILURES PRESENT"; exit 1; }
