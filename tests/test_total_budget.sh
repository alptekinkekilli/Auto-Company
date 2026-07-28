#!/usr/bin/env bash
# Tests for the combined Claude+Codex spend ceiling (TOTAL_BUDGET_USD).
#
#   bash tests/test_total_budget.sh scripts/core/auto-loop.sh
#
# The property that matters most: a FAILED codex measurement must never read as
# $0, because that would silently switch the ceiling off — the one failure mode
# a budget guard cannot have.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT
mkdir -p "$SB/bin"

# stub ccusage: emits two sessions, one before and one after the anchor
make_ccusage() {  # <mode: ok|fail>
    if [ "$1" = "ok" ]; then
        cat > "$SB/bin/ccusage" <<'EOS'
#!/usr/bin/env bash
cat <<'JSON'
{"sessions":[
 {"costUSD": 5.00, "lastActivity": "2000-01-01T00:00:00.000Z"},
 {"costUSD": 7.25, "lastActivity": "2099-01-01T00:00:00.000Z"}
]}
JSON
EOS
    else
        printf '#!/usr/bin/env bash\nexit 1\n' > "$SB/bin/ccusage"
    fi
    chmod +x "$SB/bin/ccusage"
}

run_codex_spend() {  # echoes "<value>|<stale flag>"
    PATH="$SB/bin:$PATH" bash -c '
        set -euo pipefail
        LOG_DIR="'"$SB"'"; WINDOW_SECONDS=18000
        OPERATOR_USAGE_FILE="'"$SB"'/nonexistent.json"; OPERATOR_USAGE_STALE_SECS=900
        '"$(awk '/^_window_anchor_epoch\(\)/,/^}/' "$SRC")"'
        CODEX_SPEND_CACHE="$LOG_DIR/.codex-spend-cache"
        '"$(awk '/^codex_window_spend\(\)/,/^}/' "$SRC")"'
        raw="$(codex_window_spend)"
        printf "%s|%s" "${raw%% *}" "${raw##* }"
    ' 2>/dev/null
}

echo "--- 1: ccusage works — only sessions inside the window are counted ---"
make_ccusage ok
out="$(run_codex_spend)"
check "codex window usd" "${out%%|*}" "7.2500"
check "not stale"        "${out##*|}" "0"

echo "--- 2: ccusage FAILS — must reuse the cached value, NOT report 0 ---"
make_ccusage fail
out="$(run_codex_spend)"
check "reused cache"  "${out%%|*}" "7.2500"
check "flagged stale" "${out##*|}" "1"

echo "--- 3: ccusage fails with NO cache — reports 0 but still flags stale ---"
rm -f "$SB/.codex-spend-cache"
out="$(run_codex_spend)"
check "zero"          "${out%%|*}" "0"
check "flagged stale" "${out##*|}" "1"

echo "--- 4: the cap arithmetic itself (claude + codex vs cap) ---"
over() { awk -v s="$1" -v b="$2" 'BEGIN { exit !(s + 0 >= b + 0) }' && echo over || echo under; }
check "34.22 + 7.25 vs 100"   "$(over "$(awk 'BEGIN{printf "%.4f",34.22+7.25}')" 100)" "under"
check "60.00 + 45.00 vs 100"  "$(over "$(awk 'BEGIN{printf "%.4f",60+45}')" 100)"      "over"
check "exactly 100 is over"   "$(over 100 100)" "over"

echo; [ "$fail" = 0 ] && echo "ALL PASS" || { echo "FAILURES"; exit 1; }
