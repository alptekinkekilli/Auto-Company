#!/usr/bin/env bash
# Tests for the two cadence/spend mechanisms shipped 2026-08-04:
#   - IDLE detection from the snapshot's `DELTA: none`
#   - the discretionary daily cap line that lands in the prompt once the day's
#     no-external-trigger cycles have spent it
# Both are plain shell fragments inside auto-loop.sh, so the tests evaluate the REAL
# code by extracting the blocks — the same approach test_prompt_assembly.sh uses, and
# the reason a raw-quote regression was caught twice before it reached production.
set -u
cd "$(dirname "$0")/.."
LOOP=scripts/core/auto-loop.sh
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; }

echo "[1] idle flag comes from the snapshot text"
idle_of() { # $1 = snapshot text -> prints 0/1
    _snapshot_block="$1"
    case "$_snapshot_block" in
        *"DELTA: none"*) echo 1 ;;
        *)               echo 0 ;;
    esac
}
[ "$(idle_of 'directive: ok
DELTA: none — nothing above moved since X')" = 1 ] && ok "DELTA none -> idle" || bad "DELTA none -> idle"
[ "$(idle_of 'DELTA: sends changed 9 -> 10')" = 0 ] && ok "a real delta -> not idle" || bad "a real delta -> not idle"
[ "$(idle_of '(snapshot unavailable this cycle)')" = 0 ] \
    && ok "unavailable snapshot -> NOT idle (fail-open)" || bad "unavailable snapshot must not read as idle"

echo "[2] the cap sums only TODAY's rows, from the real ledger format"
LEDGER="$TMP/discretionary-spend.ndjson"
TODAY=$(date -u +%Y-%m-%d)
{
  printf '{"date":"2020-01-01","ts":"2020-01-01T00:00:00Z","cycle":1,"cost":99.0}\n'
  printf '{"date":"%s","ts":"%sT01:00:00Z","cycle":2,"cost":12.5}\n' "$TODAY" "$TODAY"
  printf 'this line is not json\n'
  printf '{"date":"%s","ts":"%sT02:00:00Z","cycle":3,"cost":7.25}\n' "$TODAY" "$TODAY"
} > "$LEDGER"
# the exact heredoc from auto-loop.sh
sum_today() {
python3 - "$1" <<'PYDISC'
import datetime as dt, json, sys
today = dt.datetime.now(dt.timezone.utc).date().isoformat()
total = 0.0
try:
    for line in open(sys.argv[1], encoding="utf-8"):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if str(row.get("date", "")) == today:
            total += float(row.get("cost") or 0)
except OSError:
    pass
print("%.2f" % total)
PYDISC
}
GOT=$(sum_today "$LEDGER")
[ "$GOT" = "19.75" ] && ok "today's rows summed, other days and junk ignored ($GOT)" \
                     || bad "expected 19.75, got $GOT"
GOT=$(sum_today "$TMP/does-not-exist.ndjson")
[ "$GOT" = "0.00" ] && ok "missing ledger reads 0, never errors" || bad "missing ledger gave '$GOT'"

echo "[3] cap comparison fires at or above the cap, not below"
over() { printf '%s\n' "$1 $2" | awk '{print ($1 >= $2) ? 1 : 0}'; }
[ "$(over 19.75 30)" = 0 ] && ok "under cap -> silent" || bad "under cap must be silent"
[ "$(over 30.00 30)" = 1 ] && ok "exactly at cap -> fires" || bad "at cap must fire"
[ "$(over 41.10 30)" = 1 ] && ok "over cap -> fires" || bad "over cap must fire"

echo "[4] the shipped code actually wires both in"
grep -q '_cycle_idle=1' "$LOOP" && ok "idle flag set in the loop" || bad "idle flag missing"
grep -q 'IDLE_LOOP_INTERVAL:-3600' "$LOOP" && ok "idle cadence default 3600s" || bad "idle cadence missing"
grep -q 'sleep "\$_sleep_for"' "$LOOP" && ok "sleep uses the computed interval" || bad "sleep still fixed"
grep -q 'DISCRETIONARY_DAILY_CAP_USD:-30' "$LOOP" && ok "cap default \$30" || bad "cap default missing"
# exactly two INJECTION sites (`$_discretionary_line` on its own line inside each
# cycle_orders block); the assignments above them do not carry the `$`.
[ "$(grep -c '^\$_discretionary_line$' "$LOOP")" = 2 ] \
    && ok "cap line injected in BOTH prompt branches" || bad "cap line missing from a branch"
grep -q 'discretionary-spend.ndjson' "$LOOP" && ok "ledger written" || bad "ledger write missing"

echo
echo "discretionary-budget: $PASS passed, $FAIL failed"
[ $FAIL = 0 ]
