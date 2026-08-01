#!/usr/bin/env bash
# Regression tests for the killed-cycle model hint (scripts/core/engine-usage-cost.py).
#
#   bash tests/test_cost_model_hint.sh
#
# Why this exists: a watchdog-killed cycle produces a stream with REAL token events but
# NO `done` event, so the adapter had no model name and priced at the unknown-model row
# × 5.0. Measured 2026-08-01: one timed-out cycle booked $63.63 against a real ~$12.7 and
# filled 64% of the 5h Claude window by itself, which suppressed the effort ladder for
# hours. The hint fixes that WITHOUT loosening the fail-closed guarantees, and these
# tests pin exactly where the line is:
#   1. no hint + no done          -> conservative row (unchanged)
#   2. valid hint + no done       -> real tariff, estimated:true, basis says HINT
#   3. UNRECOGNISED hint + no done-> still conservative (a bad hint cannot cheapen a cycle)
#   4. done present               -> done.model WINS, hint ignored, estimated:false
# (4) is the important one: the hint must never override what actually ran, or the
# model-substitution guard would be silently defeated on every priced cycle.
set -uo pipefail
ADAPTER="${1:-scripts/core/engine-usage-cost.py}"
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in '$2'"; fail=1 ;; esac; }
not_contains() { case "$2" in *"$3"*) echo "  FAIL $1: unexpected '$3'"; fail=1 ;; *) echo "  PASS $1" ;; esac; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

TOK='{"type":"tokens","input":1000,"output":500,"cache_read_input":2000000,"cache_creation_input":100000}'
printf '%s\n' "$TOK" > "$WORK/killed.ndjson"
printf '%s\n{"type":"done","model":"claude-sonnet-5"}\n' "$TOK" > "$WORK/complete.ndjson"

cost_of() { printf '%s' "$1" | python3 -c 'import json,sys; print(json.load(sys.stdin)["cost_usd"])'; }

echo "--- 1: no hint, no done event — conservative row unchanged ---"
out=$(python3 "$ADAPTER" --ndjson-file "$WORK/killed.ndjson")
contains "unknown model"      "$out" '"model": "unknown"'
contains "conservative basis" "$out" "UNKNOWN MODEL"
contains "flagged estimated"  "$out" '"estimated": true'
base_cost=$(cost_of "$out")

echo "--- 2: valid hint, no done event — real tariff, still flagged ---"
out=$(python3 "$ADAPTER" --ndjson-file "$WORK/killed.ndjson" --model-hint claude-sonnet-5)
contains "hinted model used"  "$out" '"model": "claude-sonnet-5"'
contains "basis names hint"   "$out" "requested-model HINT"
contains "never calibrated"   "$out" '"estimated": true'
hint_cost=$(cost_of "$out")
python3 -c "
import sys
base, hint = float('$base_cost'), float('$hint_cost')
ok = hint < base / 4
print(('  PASS hint removes the phantom (%.4f vs %.4f)' if ok else '  FAIL hint did not cut cost (%.4f vs %.4f)') % (hint, base))
sys.exit(0 if ok else 1)
" || fail=1

echo "--- 3: UNRECOGNISED hint — still conservative (bad hint cannot cheapen) ---"
out=$(python3 "$ADAPTER" --ndjson-file "$WORK/killed.ndjson" --model-hint totally-made-up-model)
contains "conservative retained" "$out" "UNKNOWN MODEL"
bad_cost=$(cost_of "$out")
if [ "$bad_cost" = "$base_cost" ]; then echo "  PASS priced identically to no-hint"; else echo "  FAIL $bad_cost != $base_cost"; fail=1; fi

echo "--- 4: done event present — done.model WINS, hint ignored ---"
out=$(python3 "$ADAPTER" --ndjson-file "$WORK/complete.ndjson" --model-hint claude-haiku-4-5-20251001)
contains     "actual model kept"  "$out" '"model": "claude-sonnet-5"'
not_contains "no hint marker"     "$out" "requested-model HINT"
contains     "stays calibrated"   "$out" '"estimated": false'

echo
if [ "$fail" = "0" ]; then echo "ALL PASS"; else echo "FAILURES"; exit 1; fi
