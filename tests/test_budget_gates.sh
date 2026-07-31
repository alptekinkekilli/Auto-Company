#!/usr/bin/env bash
# The 15 required tests from the APP-263 budget decision (2026-07-30).
#
#   bash tests/test_budget_gates.sh scripts/core/auto-loop.sh
#
# Functions are extracted from the source with awk (same harness pattern as
# test_total_budget.sh), ccusage is a PATH stub, and "now" is pinned through
# BUDGET_NOW_OVERRIDE so period boundaries are deterministic without faketime.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }
check_contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT
mkdir -p "$SB/bin"

# Pinned clock: 2026-08-05 12:00:00 UTC (mid-day, mid-week — both boundaries visible)
NOW=1786017600
DAY_START=$(( NOW - (NOW % 86400) ))
WEEK_AGO=$(( NOW - 604800 ))

# ccusage stub: reads $SB/ccusage.json; exit 1 when absent (failure mode).
cat > "$SB/bin/ccusage" <<EOS
#!/usr/bin/env bash
[ -f "$SB/ccusage.json" ] || exit 1
cat "$SB/ccusage.json"
EOS
chmod +x "$SB/bin/ccusage"

iso() { python3 -c "import datetime,sys; print(datetime.datetime.fromtimestamp(int(sys.argv[1]), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'))" "$1"; }
utc() { python3 -c "import datetime,sys; print(datetime.datetime.fromtimestamp(int(sys.argv[1]), datetime.timezone.utc).strftime(sys.argv[2]))" "$1" "$2"; }

# Assemble the harness: extracted functions + stubs, driven per-test via env.
extract() { awk "/^$1\(\) \{/,/^\}/" "$SRC"; }
HARNESS="$SB/harness.sh"
{
    echo 'set -uo pipefail'
    echo "LOG_DIR=\"$SB\"; WINDOW_SECONDS=18000; BUDGET_PAUSE_SECONDS=1800"
    echo "OPERATOR_USAGE_FILE=\"$SB/operator-usage.json\"; OPERATOR_USAGE_STALE_SECS=900"
    echo "SPEND_LEDGER=\"$SB/spend-window.log\"; TOTAL_SPEND_LEDGER=\"$SB/spend-total.log\""
    echo "TOTAL_LEDGER_RETENTION_DAYS=90; ANALYST_SESSIONS_FILE=\"$SB/analyst-codex-sessions.log\""
    echo "CODEX_SPEND_CACHE=\"$SB/.codex-spend-cache\"; ROUTER_STATE_FILE=\"$SB/router-state\""
    echo "LOOP_BOOT_ID=test-boot; loop_count=1; SCRIPT_DIR=\"$SB\""
    echo "CODEX_DISABLED=\"\${CODEX_DISABLED:-0}\"; RESOLVED_CODEX_BIN=\"\${RESOLVED_CODEX_BIN:-/bin/true}\""
    echo "CODEX_WINDOW_LIMIT=\"\${CODEX_WINDOW_LIMIT:-}\"; ENGINE=\"\${ENGINE:-claude}\"; ROUTER_ALTERNATE=\"\${ROUTER_ALTERNATE:-1}\""
    echo "CLAUDE_5H_BUDGET_USD=\"\${CLAUDE_5H_BUDGET_USD:-}\"; CODEX_5H_BUDGET_USD=\"\${CODEX_5H_BUDGET_USD:-}\""
    echo "TOTAL_DAILY_BUDGET_USD=\"\${TOTAL_DAILY_BUDGET_USD:-}\"; TOTAL_WEEKLY_BUDGET_USD=\"\${TOTAL_WEEKLY_BUDGET_USD:-}\""
    echo "WINDOW_BUDGET_USD=\"\${WINDOW_BUDGET_USD:-}\"; TOTAL_BUDGET_USD=\"\${TOTAL_BUDGET_USD:-}\""
    echo 'log() { echo "$@"; }'
    echo "LOOP_HOLD_FILE=\"$SB/LOOP_HOLD\""
    echo 'latch_budget_hold() { echo "LATCHED: $1" > "$LOOP_HOLD_FILE"; }'
    echo 'resolve_codex_bin() { echo /bin/true; }'
    echo 'codex_window_count() { echo 0; }'
    echo '_router_persist() { echo "$1" > "$ROUTER_STATE_FILE"; }'
    for f in _budget_now _utc_day_start _fmt_utc _window_anchor_epoch window_spend \
             record_total_spend claude_spend_since codex_ledger_spend_since _max_usd _sum_usd \
             _codex_spend_since \
             _codex_spend_entries_since _weekly_resume_epoch _notify_gate_block_once \
             evaluate_budget_gates select_cycle_engine; do
        extract "$f"
        echo ""
    done
} > "$HARNESS"

run() { # env overrides via leading VAR=... args, then a snippet
    PATH="$SB/bin:$PATH" BUDGET_NOW_OVERRIDE="$NOW" bash -c "source '$HARNESS'; $1" 2>&1
}

reset_state() {
    rm -f "$SB"/spend-window.log "$SB"/spend-total.log "$SB"/analyst-codex-sessions.log \
          "$SB"/.codex-spend-cache-* "$SB"/router-state "$SB"/.gate-notified-* "$SB"/ccusage.json
}

codex_json() { # $@ = "cost:epoch[:sessionFile]" triples
    {
        echo '{"sessions":['
        local first=1 c e sf
        for spec in "$@"; do
            c="${spec%%:*}"; rest="${spec#*:}"; e="${rest%%:*}"; sf="${rest#*:}"
            [ "$sf" = "$e" ] && sf="rollout-plain-$e"
            [ $first -eq 0 ] && echo ','
            first=0
            printf '{"costUSD": %s, "lastActivity": "%s", "sessionFile": "%s"}' "$c" "$(iso "$e")" "$sf"
        done
        echo ']}'
    } > "$SB/ccusage.json"
}

echo "--- 1: Claude at \$100 blocks Claude; eligible Codex is routed ---"
reset_state
# claude 5h derives from the TOTAL ledger now (REVISE-2 gate A3)
printf '%s claude run-t1a 50.0\n%s claude run-t1b 50.0\n' "$((NOW - 600))" "$((NOW - 600))" > "$SB/spend-total.log"
codex_json "1.0:$((NOW - 300))"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 TOTAL_DAILY_BUDGET_USD=500 TOTAL_WEEKLY_BUDGET_USD=2500 select_cycle_engine; echo "action=$CYCLE_ROUTER_ACTION override=$CYCLE_ENGINE_OVERRIDE"; echo "$CYCLE_ROUTER_MSG"')"
check_contains "routes codex"        "$out" "action=run override=codex"
check_contains "names CLAUDE_5H"     "$out" "[GATE] CLAUDE_5H"
check_contains "notional disclaimer" "$out" "not billed cash"

echo "--- 2: Codex at \$100 blocks Codex; eligible Claude is routed ---"
reset_state
echo "$((NOW - 600)) claude run-t2 1.0" > "$SB/spend-total.log"
codex_json "100.5:$((NOW - 300))"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 select_cycle_engine; echo "action=$CYCLE_ROUTER_ACTION override=$CYCLE_ENGINE_OVERRIDE"; echo "$CYCLE_ROUTER_MSG"')"
check_contains "runs claude"     "$out" "action=run override="
check_contains "names CODEX_5H"  "$out" "[GATE] CODEX_5H"
check "state persisted claude" "$(cat "$SB/router-state")" "claude"

echo "--- 3: both engine gates blocked -> pause until earliest reset ---"
reset_state
echo "$((NOW - 600)) claude run-t3 150.0" > "$SB/spend-total.log"
codex_json "120.0:$((NOW - 300))"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 select_cycle_engine; echo "action=$CYCLE_ROUTER_ACTION"; echo "$CYCLE_ROUTER_MSG"')"
check_contains "paused"          "$out" "action=pause"
check_contains "both gates named" "$out" "CLAUDE_5H + CODEX_5H"
check_contains "resume time"      "$out" "Resume: $(utc "$NOW" %Y-%m-%dT)"

echo "--- 4: one engine's rollover does not reset the other's counter ---"
reset_state
# Claude window rolled: only an out-of-window ledger row. Codex sessions unchanged.
echo "$((NOW - 21600)) claude run-t4old 9.9" > "$SB/spend-total.log"
codex_json "42.0:$((NOW - 300))"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 evaluate_budget_gates >/dev/null; echo "c=$BG_CLAUDE5 x=$BG_CODEX5"')"
check "claude rolled to 0"    "${out##*c=}" "0.0000 x=42.0000"
# And the mirror: codex empty, claude carries
codex_json "0.0:$((NOW - 700000))"   # only an out-of-window session
echo "$((NOW - 600)) claude run-t4b 7.5" > "$SB/spend-total.log"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 evaluate_budget_gates >/dev/null; echo "c=$BG_CLAUDE5 x=$BG_CODEX5"')"
check "codex 0, claude kept" "${out##*c=}" "7.5000 x=0.0000"

echo "--- 5: a 5h rollover does not reset DAILY or WEEKLY ---"
reset_state
echo "$((NOW - 21600)) claude run-a 30.0" > "$SB/spend-total.log"   # 6h ago: outside 5h, same UTC day
codex_json "20.0:$((NOW - 21600))"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 TOTAL_WEEKLY_BUDGET_USD=2500 evaluate_budget_gates >/dev/null; echo "d=$BG_DAILY w=$BG_WEEKLY"')"
check "daily survives roll"  "${out##*d=}" "50.0000 w=50.0000"

echo "--- 6: UTC day rollover resets DAILY only ---"
reset_state
Y=$(( DAY_START - 3600 ))                        # yesterday 23:00 UTC
echo "$Y claude run-y 40.0" > "$SB/spend-total.log"
codex_json "25.0:$Y"
out="$(run 'TOTAL_DAILY_BUDGET_USD=500 TOTAL_WEEKLY_BUDGET_USD=2500 evaluate_budget_gates >/dev/null; echo "d=$BG_DAILY w=$BG_WEEKLY"')"
check "daily excludes yesterday, weekly keeps it" "${out##*d=}" "0.0000 w=65.0000"

echo "--- 7: rolling WEEKLY expires entry-by-entry, no calendar-week reset ---"
reset_state
OLD=$(( NOW - 604800 - 3600 ))   # 7d1h ago -> expired
NEWER=$(( NOW - 604800 + 3600 )) # 6d23h ago -> still counted
printf '%s claude run-old 100.0\n%s claude run-new 60.0\n' "$OLD" "$NEWER" > "$SB/spend-total.log"
codex_json "0.0:$((NOW - 999999999))"
out="$(run 'TOTAL_WEEKLY_BUDGET_USD=2500 evaluate_budget_gates >/dev/null; echo "w=$BG_WEEKLY"')"
check "only 6d23h entry counted" "${out##*w=}" "60.0000"

echo "--- 8: DAILY at \$500 blocks both and reports next UTC midnight ---"
reset_state
echo "$((NOW - 3600)) claude run-big 480.0" > "$SB/spend-total.log"
codex_json "30.0:$((NOW - 3600))"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 TOTAL_DAILY_BUDGET_USD=500 TOTAL_WEEKLY_BUDGET_USD=2500 select_cycle_engine; echo "action=$CYCLE_ROUTER_ACTION"; echo "$CYCLE_ROUTER_MSG"')"
check_contains "paused"            "$out" "action=pause"
check_contains "gate type"         "$out" "[GATE] DAILY_TOTAL"
check_contains "both engines"      "$out" "BOTH engines"
check_contains "exact UTC midnight" "$out" "Resume: $(utc "$((DAY_START + 86400))" %Y-%m-%dT%H:%M:%SZ)"
check_contains "no generic 5h msg" "$out" "next UTC midnight"

echo "--- 9: WEEKLY at \$2500 blocks both and reports the spend-expiry time ---"
reset_state
E1=$(( NOW - 500000 )); E2=$(( NOW - 400000 ))
printf '%s claude run-w1 1500.0\n%s claude run-w2 1200.0\n' "$E1" "$E2" > "$SB/spend-total.log"
codex_json "0.0:$((NOW - 999999999))"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 TOTAL_WEEKLY_BUDGET_USD=2500 select_cycle_engine; echo "action=$CYCLE_ROUTER_ACTION"; echo "$CYCLE_ROUTER_MSG"')"
check_contains "paused"     "$out" "action=pause"
check_contains "gate type"  "$out" "[GATE] WEEKLY_TOTAL"
# dropping run-w1 (oldest) brings 2700->1200 < 2500, so resume = E1 + 7d
check_contains "computed expiry" "$out" "Resume: $(utc "$((E1 + 604800))" %Y-%m-%dT%H:%M:%SZ)"

echo "--- 10: duplicate Claude run_id is counted once in every period ---"
reset_state
run 'record_total_spend claude dup-1 5.0; record_total_spend claude dup-1 5.0; record_total_spend claude dup-2 2.0' >/dev/null
check "ledger rows"  "$(wc -l < "$SB/spend-total.log" | tr -d ' ')" "2"
out="$(run 'claude_spend_since 0')"
check "summed once"  "$out" "7.0000"

echo "--- 11: a VERIFIED analyst session is excluded from 5h, DAILY and WEEKLY ---"
reset_state
AUUID="019fb10b-224a-7b21-9952-7bf39bc56da2"
echo "$NOW $AUUID" > "$SB/analyst-codex-sessions.log"
codex_json "50.0:$((NOW - 300)):rollout-2026-08-05T10-00-00-$AUUID" "10.0:$((NOW - 300))"
out="$(run 'CODEX_5H_BUDGET_USD=100 TOTAL_DAILY_BUDGET_USD=500 TOTAL_WEEKLY_BUDGET_USD=2500 evaluate_budget_gates >/dev/null; echo "x=$BG_CODEX5 d=$BG_DAILY w=$BG_WEEKLY"')"
check "excluded everywhere" "${out##*x=}" "10.0000 d=10.0000 w=10.0000"

echo "--- 12: missing/ambiguous analyst metadata is INCLUDED (fail closed) ---"
reset_state
printf 'not-a-valid-line\n%s short-id\n' "$NOW" > "$SB/analyst-codex-sessions.log"
codex_json "50.0:$((NOW - 300)):rollout-2026-08-05T10-00-00-$AUUID" "10.0:$((NOW - 300))"
out="$(run 'CODEX_5H_BUDGET_USD=100 evaluate_budget_gates >/dev/null; echo "x=$BG_CODEX5"')"
check "nothing excluded" "${out##*x=}" "60.0000"

echo "--- 13: STALE fallback cannot reduce an already-observed total ---"
reset_state
codex_json "77.0:$((NOW - 300))"
run 'evaluate_budget_gates >/dev/null' >/dev/null          # primes per-gate caches
rm -f "$SB/ccusage.json"                                   # ccusage now fails
out="$(run 'CODEX_5H_BUDGET_USD=100 evaluate_budget_gates 2>/dev/null; echo "x=$BG_CODEX5"')"
check "reused observed value" "${out##*x=}" "77.0000"
out="$(run 'CODEX_5H_BUDGET_USD=100 evaluate_budget_gates 2>/dev/null' | head -1)"
check_contains "flags stale in status line" "$out" "STALE"

echo "--- 14: Alternate stays deterministic across eligibility states ---"
reset_state
echo "$((NOW - 600)) claude run-t14 1.0" > "$SB/spend-total.log"
codex_json "1.0:$((NOW - 300))"
echo claude > "$SB/router-state"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 select_cycle_engine; echo "override=$CYCLE_ENGINE_OVERRIDE"')"
check_contains "claude->codex toggle" "$out" "override=codex"
check "state now codex" "$(cat "$SB/router-state")" "codex"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 select_cycle_engine; echo "override=$CYCLE_ENGINE_OVERRIDE"')"
check_contains "codex->claude toggle" "$out" "override="
# codex becomes blocked -> claude runs and holds state; on reopen the toggle resumes
codex_json "150.0:$((NOW - 300))"
run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 select_cycle_engine' >/dev/null
check "blocked codex skipped, state claude" "$(cat "$SB/router-state")" "claude"
codex_json "1.0:$((NOW - 300))"
out="$(run 'CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 select_cycle_engine; echo "override=$CYCLE_ENGINE_OVERRIDE"')"
check_contains "deterministic resume to codex" "$out" "override=codex"

echo "--- 15: deprecated variables warn and cannot override the new gates ---"
reset_state
# behavioral: old vars set at values that WOULD have gated under the old model
echo "$((NOW - 600)) claude run-t15 50.0" > "$SB/spend-total.log"
codex_json "1.0:$((NOW - 300))"
out="$(run 'WINDOW_BUDGET_USD=1 TOTAL_BUDGET_USD=1 CLAUDE_5H_BUDGET_USD=100 CODEX_5H_BUDGET_USD=100 select_cycle_engine; echo "action=$CYCLE_ROUTER_ACTION"')"
check_contains "old vars do not gate" "$out" "action=run"
# static: the startup warning exists and names both variables as IGNORED
w="$(grep -c 'DEPRECATED\].*is set but IGNORED' "$SRC")"
check "startup warnings present" "$w" "2"

echo ""
[ "$fail" -eq 0 ] && echo "ALL 15 GATE TESTS PASS" || echo "FAILURES PRESENT"
exit "$fail"
