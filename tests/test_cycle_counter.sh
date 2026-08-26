#!/usr/bin/env bash
# COUNTER: the cycle counter must be MONOTONIC ACROSS REDEPLOYS.
#
#   bash tests/test_cycle_counter.sh [scripts/core/auto-loop.sh]
#
# Runs the REAL seed block (init) and persist line (per-cycle) extracted from auto-loop.sh
# against a throwaway LOG_DIR, so a regression in either fails here instead of silently
# resetting Cycle #N to #1 on the next boot.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check(){ if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: want '$3' got '$2'"; fail=1; fi; }

# Extract the seed block (CYCLE_COUNTER_FILE= .. loop_count=) into a runnable stub.
SEED="$(sed -n '/^CYCLE_COUNTER_FILE=/,/^loop_count=/p' "$SRC")"
[ -n "$SEED" ] || { echo "FAIL: could not extract seed block"; exit 1; }
STUB="$(mktemp)"; { echo 'LOG_DIR="$1"'; printf '%s\n' "$SEED"; echo 'echo "$loop_count"'; } > "$STUB"
seed(){ bash "$STUB" "$1"; }

echo "--- 1: fresh dir (no counter, no logs) → 0 (fail-safe) ---"
d="$(mktemp -d)"; check "seed=0" "$(seed "$d")" "0"

echo "--- 2: persisted counter file wins ---"
d="$(mktemp -d)"; echo 42 > "$d/.cycle-counter"; check "seed=42" "$(seed "$d")" "42"

echo "--- 3: no counter file, but cycle-NNNN logs on disk → highest (self-heal) ---"
d="$(mktemp -d)"; : > "$d/cycle-0007-20260826-120000.log"; : > "$d/cycle-0003-x.log"
check "seed=7" "$(seed "$d")" "7"

echo "--- 4: both present → max(file, logs) ---"
d="$(mktemp -d)"; echo 5 > "$d/.cycle-counter"; : > "$d/cycle-0009-x.log"
check "seed=9" "$(seed "$d")" "9"

echo "--- 5: corrupt counter file → digits-only strip, falls to logs/0 ---"
d="$(mktemp -d)"; printf 'nonsense\n' > "$d/.cycle-counter"; check "seed=0" "$(seed "$d")" "0"

echo "--- 6: persist line writes the new value ---"
PERSIST="$(grep -F 'CYCLE_COUNTER_FILE.tmp' "$SRC" | head -1)"
[ -n "$PERSIST" ] || { echo "FAIL: could not extract persist line"; exit 1; }
d="$(mktemp -d)"; CYCLE_COUNTER_FILE="$d/.cycle-counter" loop_count=8 bash -c '
  CYCLE_COUNTER_FILE="'"$d"'/.cycle-counter"; loop_count=8; '"$PERSIST"
check "file=8 after persist" "$(cat "$d/.cycle-counter" 2>/dev/null)" "8"

echo "--- 7: seed after persist resumes from persisted (redeploy sim) ---"
check "seed=8 (resume)" "$(seed "$d")" "8"

echo; [ "$fail" = 0 ] && echo "ALL PASS" || { echo "FAILURES"; exit 1; }
