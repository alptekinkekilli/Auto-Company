#!/usr/bin/env bash
# IDLE-SKIP regression suite (2026-08-06).
#
# Two units, tested separately because they fail in different ways:
#   1. `_idle_skip_due` — extracted verbatim from auto-loop.sh (same technique as
#      test_active_window.sh) so the test drives the SHIPPING code, not a copy.
#   2. scripts/ops/idle-skip-note.py — one consensus line per UTC day, updated in place.
#
# The property that must not regress: the first cycle of a UTC day is NEVER skipped.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOOP="$ROOT/scripts/core/auto-loop.sh"
NOTE="$ROOT/scripts/ops/idle-skip-note.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0; fail=0
ok()   { pass=$((pass+1)); printf '  ok   %s\n' "$1"; }
bad()  { fail=$((fail+1)); printf '  FAIL %s\n' "$1"; }
check(){ if [ "$2" = "$3" ]; then ok "$1"; else bad "$1 (want=$3 got=$2)"; fi; }

# ---------- unit 1: _idle_skip_due, extracted from the real script ----------
awk '/^    _idle_skip_due\(\) \{/,/^    \}/' "$LOOP" | sed 's/^    //' > "$TMP/fn.sh"
[ -s "$TMP/fn.sh" ] || { echo "FATAL: could not extract _idle_skip_due from $LOOP"; exit 1; }
# shellcheck disable=SC1090
. "$TMP/fn.sh"

STAMP="$TMP/last-full-cycle.date"
TODAY="2026-08-06"

due() { if _idle_skip_due "$1" "$STAMP" "$TODAY"; then echo yes; else echo no; fi; }

echo "== _idle_skip_due =="

rm -f "$STAMP"
check "first cycle of the day (no stamp) is NEVER skipped" "$(due 1)" "no"

echo "2026-08-05" > "$STAMP"
check "yesterday's stamp does not authorize a skip" "$(due 1)" "no"

echo "$TODAY" > "$STAMP"
check "idle + today's full cycle done -> skip" "$(due 1)" "yes"
check "not idle -> full cycle even with today's stamp" "$(due 0)" "no"
check "missing idle arg defaults to not-idle" "$(_idle_skip_due "" "$STAMP" "$TODAY" && echo yes || echo no)" "no"

IDLE_SKIP_ENABLED=0
check "kill switch disables skipping" "$(due 1)" "no"
IDLE_SKIP_ENABLED=1
check "kill switch back on" "$(due 1)" "yes"
unset IDLE_SKIP_ENABLED
check "unset kill switch defaults to enabled" "$(due 1)" "yes"

printf '' > "$STAMP"
check "empty stamp file does not authorize a skip" "$(due 1)" "no"

echo "$TODAY" > "$STAMP"
check "unreadable stamp path does not authorize a skip" \
      "$(_idle_skip_due 1 "$TMP/definitely-missing" "$TODAY" && echo yes || echo no)" "no"

# ---------- unit 2: consensus note ----------
echo "== idle-skip-note.py =="
CONS="$TMP/consensus.md"
printf '# Consensus\n\n## Next Action\nwait for a reply\n' > "$CONS"
BEFORE_HEAD="$(head -3 "$CONS")"

python3 "$NOTE" --consensus "$CONS" --day "$TODAY" --time "07:04" >/dev/null
check "first skip adds exactly one line" "$(grep -c 'idle-skip:2026-08-06' "$CONS")" "1"
check "count starts at 1" "$(grep -c '1 cycle skipped' "$CONS")" "1"
check "existing content preserved" "$(head -3 "$CONS")" "$BEFORE_HEAD"

python3 "$NOTE" --consensus "$CONS" --day "$TODAY" --time "08:04" >/dev/null
python3 "$NOTE" --consensus "$CONS" --day "$TODAY" --time "09:04" >/dev/null
check "still exactly one line for the day" "$(grep -c 'idle-skip:2026-08-06' "$CONS")" "1"
check "count incremented to 3" "$(grep -c '3 cycles skipped' "$CONS")" "1"
check "start time is the FIRST skip" "$(grep -c '(07:04→09:04 UTC)' "$CONS")" "1"

python3 "$NOTE" --consensus "$CONS" --day "2026-08-07" --time "07:10" >/dev/null
check "a new day gets its own line" "$(grep -c 'idle-skip:' "$CONS")" "2"
check "yesterday's line untouched" "$(grep -c '3 cycles skipped' "$CONS")" "1"

python3 "$NOTE" --consensus "$TMP/nope.md" --day "$TODAY" --time "07:04" >/dev/null 2>&1
check "missing consensus exits non-zero" "$?" "1"
check "no stray temp files left behind" "$(find "$TMP" -name '.idle-skip-*' | wc -l | tr -d ' ')" "0"

# consensus must still be valid markdown-ish: the note is a single line, not a block
check "note is one physical line" \
      "$(grep -c '^- \*\*Idle watch 2026-08-06' "$CONS")" "1"

# ---------- unit 3: wiring in auto-loop.sh ----------
echo "== wiring =="
check "skip branch calls no model" \
      "$(awk '/_idle_skip_due "\$_cycle_idle"/,/^    fi$/' "$LOOP" | grep -cE 'run_engine|claude |codex ')" "0"
check "skip branch continues the loop" \
      "$(awk '/_idle_skip_due "\$_cycle_idle"/,/^    fi$/' "$LOOP" | grep -c 'continue')" "1"
check "stamp is written only on success" \
      "$(grep -c 'if \[ -z "\${cycle_failed_reason:-}" \]; then' "$LOOP")" "1"
check "stamp file path agrees on both sides" \
      "$(grep -c 'last-full-cycle.date' "$LOOP")" "2"

echo
echo "passed=$pass failed=$fail"
[ "$fail" -eq 0 ]
