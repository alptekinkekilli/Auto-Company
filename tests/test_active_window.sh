#!/usr/bin/env bash
# Tests for the business-hours gate (LOOP_ACTIVE_WINDOW_UTC), shipped 2026-08-04.
# Extracts the REAL _window_active() from auto-loop.sh rather than a copy, and drives
# it with a stubbed `date` so every hour can be tested without waiting for the clock.
set -u
cd "$(dirname "$0")/.."
LOOP=scripts/core/auto-loop.sh
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; }

# pull the function out of the shipped script (start marker -> closing brace)
awk '/^_window_active\(\) \{/,/^\}/' "$LOOP" > "$TMP/fn.sh"
[ -s "$TMP/fn.sh" ] && ok "extracted _window_active from the real script" || { bad "could not extract"; exit 1; }

# harness: FAKE_HOUR drives a stubbed date -u +%H
cat > "$TMP/run.sh" <<'RUN'
date() { if [ "${1:-}" = "-u" ]; then echo "$FAKE_HOUR"; else command date "$@"; fi; }
. "$FN"
if _window_active; then echo active; else echo off; fi
RUN

check() { # desc, window, hour, expected
    got=$(LOOP_ACTIVE_WINDOW_UTC="$2" FAKE_HOUR="$3" FN="$TMP/fn.sh" bash "$TMP/run.sh")
    [ "$got" = "$4" ] && ok "$1" || bad "$1 — window=$2 hour=$3 expected $4 got $got"
}

echo "[1] the operator's window: 07-15 UTC"
check "06:xx before open -> off"      07-15 06 off
check "07:xx at open -> active"       07-15 07 active
check "14:xx last active hour"        07-15 14 active
check "15:xx at close -> off"         07-15 15 off
check "23:xx night -> off"            07-15 23 off
check "00:xx midnight -> off"         07-15 00 off

echo "[2] leading zeros are decimal, not octal (08 and 09 are the classic trap)"
check "08:xx inside"                  07-15 08 active
check "09:xx inside"                  07-15 09 active
check "08-09 window at 08"            08-09 08 active
check "08-09 window at 09"            08-09 09 off

echo "[3] a window that wraps midnight"
check "22-06 at 23 -> active"         22-06 23 active
check "22-06 at 02 -> active"         22-06 02 active
check "22-06 at 06 -> off"            22-06 06 off
check "22-06 at 12 -> off"            22-06 12 off

echo "[4] fail OPEN on anything unusable — a typo must never park the company"
check "unset -> always active"        ""      03 active
check "garbage -> active"             "mesai" 03 active
check "wrong shape -> active"         "7-15"  03 active
check "nonsense hours -> active"      "99-99" 03 active

echo "[5] the gate is wired in BEFORE the router and the cycle counter"
W=$(grep -n '_window_active' "$LOOP" | tail -1 | cut -d: -f1)
R=$(grep -n 'select_cycle_engine$' "$LOOP" | tail -1 | cut -d: -f1)
C=$(grep -n 'loop_count=\$((loop_count + 1))' "$LOOP" | head -1 | cut -d: -f1)
[ "$W" -lt "$R" ] && ok "checked before select_cycle_engine (no model/external call)" \
                  || bad "window check runs after the router ($W vs $R)"
[ "$W" -lt "$C" ] && ok "checked before the cycle counter increments" \
                  || bad "off-hours ticks would burn cycle numbers ($W vs $C)"
grep -q 'OFF_HOURS_POLL_SECONDS:-900' "$LOOP" && ok "off-hours poll default 900s" || bad "poll default missing"
grep -q '_offhours_logged' "$LOOP" && ok "logs the transition once, not every poll" || bad "would log every poll"

echo
echo "active-window: $PASS passed, $FAIL failed"
[ $FAIL = 0 ]
