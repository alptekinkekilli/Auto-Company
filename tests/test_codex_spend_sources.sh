#!/usr/bin/env bash
# Codex spend comes from TWO DISJOINT sources and must be SUMMED, per period.
#
#   bash tests/test_codex_spend_sources.sh scripts/core/auto-loop.sh
#
# Why this test exists: `ccusage` reads CODEX_HOME session files, which only the Codex
# CLI writes; the total ledger's codex rows are written only by jcode-harness codex
# cycles. Neither source can see the other's cycles. An earlier revision combined them
# with max(), which silently discarded the smaller one — under the shipping mixed
# configuration that means real spend vanishing from a gate. These cases pin the
# arithmetic for the 5h, daily and weekly periods, and pin that a jcode row is never
# double-counted by ccusage.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }

SB="$(mktemp -d)"
trap 'rm -rf "$SB"' EXIT
NOW=1785500000

# ledger rows: epoch engine run_id usd
{
    echo "$((NOW - 3600))  codex  boot-c1  2.0000"    # 1h ago  — in 5h, day, week
    echo "$((NOW - 36000)) codex  boot-c2  3.0000"    # 10h ago — in day and week only
    echo "$((NOW - 300000)) codex boot-c3  7.0000"    # ~3.5d   — week only
    echo "$((NOW - 3600))  claude boot-c4  1.0000"    # claude row must be ignored here
} > "$SB/spend-total.log"

harness() {  # $1 = ccusage-reported codex usd for the period
    {
        echo 'set -uo pipefail'
        echo "TOTAL_SPEND_LEDGER=\"$SB/spend-total.log\""
        awk '/^codex_ledger_spend_since\(\)/,/^}/' "$SRC"
        awk '/^_sum_usd\(\)/,/^}/' "$SRC"
        echo "ccusage_figure=\"$1\""
    } > "$SB/h.sh"
}

echo "--- 5h window: ccusage 4.00 (CLI cycles) + ledger 2.00 (jcode cycle) = 6.00 ---"
harness 4.0000
out=$(bash -c 'source '"$SB"'/h.sh; _sum_usd "$ccusage_figure" "$(codex_ledger_spend_since '"$((NOW - 18000))"')"')
check "5h summed" "$out" "6.0000"

echo "--- daily: ccusage 4.00 + ledger 5.00 (2.00 + 3.00) = 9.00 ---"
out=$(bash -c 'source '"$SB"'/h.sh; _sum_usd "$ccusage_figure" "$(codex_ledger_spend_since '"$((NOW - 86400))"')"')
check "daily summed" "$out" "9.0000"

echo "--- weekly: ccusage 4.00 + ledger 12.00 (2+3+7) = 16.00 ---"
out=$(bash -c 'source '"$SB"'/h.sh; _sum_usd "$ccusage_figure" "$(codex_ledger_spend_since '"$((NOW - 604800))"')"')
check "weekly summed" "$out" "16.0000"

echo "--- max() would have UNDER-read every one of those (regression pin) ---"
awk '/^_max_usd\(\)/,/^}/' "$SRC" >> "$SB/h.sh"
out=$(bash -c 'source '"$SB"'/h.sh; _max_usd "$ccusage_figure" "$(codex_ledger_spend_since '"$((NOW - 86400))"')"')
check "max is NOT the daily answer" "$out" "5.0000"   # 5.00 != 9.00: the CLI's 4.00 vanished

echo "--- claude rows never leak into the codex figure ---"
out=$(bash -c 'source '"$SB"'/h.sh; codex_ledger_spend_since '"$((NOW - 18000))")
check "claude excluded" "$out" "2.0000"

echo "--- a zero ccusage read still yields the ledger total (never zero out real spend) ---"
harness 0.0000
out=$(bash -c 'source '"$SB"'/h.sh; _sum_usd "$ccusage_figure" "$(codex_ledger_spend_since '"$((NOW - 86400))"')"')
check "empty ccusage does not erase ledger" "$out" "5.0000"

echo
if [ "$fail" -eq 0 ]; then echo "ALL CODEX-SPEND-SOURCE TESTS PASS"; else echo "FAILURES PRESENT"; exit 1; fi
