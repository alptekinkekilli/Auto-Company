#!/usr/bin/env bash
# Wiring test for the work-window brake inside scripts/core/auto-loop.sh.
# Two layers: (1) static invariants — the wiring is present and correctly formed, so a
# future edit that silently breaks it fails here; (2) contract behaviour — work-window.py
# invoked EXACTLY as the loop invokes it returns the right exit code + line.
#
# Run: bash tests/test_auto_loop_work_window.sh
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOOP="$REPO/scripts/core/auto-loop.sh"
WW="$REPO/scripts/ops/work-window.py"
fails=0
pass() { printf 'PASS %s\n' "$1"; }
fail() { printf 'FAIL %s\n' "$1"; fails=$((fails+1)); }
chk()  { if eval "$2"; then pass "$1"; else fail "$1"; fi; }

# --- Layer 1: static wiring invariants ------------------------------------------------
chk "auto-loop.sh parses (bash -n)" "bash -n '$LOOP'"

# IDLE-SKIP must be gated on the window being closed.
chk "IDLE-SKIP gated on _workwin_open != 1" \
  "grep -q '\[ \"\$_workwin_open\" != \"1\" \] && _idle_skip_due' '$LOOP'"

# The window is computed from the snapshot with a set -e safe capture.
chk "window exit captured set-e-safe (|| _workwin_rc=)" \
  "grep -q '|| _workwin_rc=\$?' '$LOOP'"

# Kill switch read LIVE from runtime.env (not a boot-frozen env only).
chk "WORK_WINDOW_ENABLED read via _read_runtime_env_key" \
  "grep -q '_read_runtime_env_key WORK_WINDOW_ENABLED' '$LOOP'"

# The order is injected into BOTH cycle_orders blocks (normal + by-reference path).
n_inject="$(grep -c '^\$_workwin_inject' "$LOOP")"
chk "\$_workwin_inject present in both cycle_orders blocks (got $n_inject)" "[ '$n_inject' = '2' ]"

# Injection is suppressed when over the discretionary cap (money backstop wins).
chk "inject gated on open AND empty discretionary line" \
  "grep -q '\[ \"\$_workwin_open\" = \"1\" \] && \[ -z \"\$_discretionary_line\" \]' '$LOOP'"

# --- Layer 2: contract behaviour at the exact call site -------------------------------
tmp="$(mktemp -d)"; mkdir -p "$tmp/logs"
call() { printf '%s' "$1" | python3 "$WW" --cycle "$2" --app "$tmp" 2>/dev/null; }

# changed -> exit 10 + line
out="$(call 'DELTA: changed=opreq_open' 5)"; rc=$?
chk "changed => exit 10" "[ '$rc' = '10' ]"
chk "changed => emits WORK-WINDOW line" "printf '%s' \"$out\" | grep -q 'WORK-WINDOW OPEN'"

# none with no window -> exit 0 + empty (fresh tmp so no state)
tmp2="$(mktemp -d)"; mkdir -p "$tmp2/logs"
out="$(printf 'DELTA: none' | python3 "$WW" --cycle 6 --app "$tmp2" 2>/dev/null)"; rc=$?
chk "none+no-window => exit 0" "[ '$rc' = '0' ]"
chk "none+no-window => empty output" "[ -z \"$out\" ]"

# corrupt state -> fail-closed exit 10
printf '{bad' > "$tmp2/logs/work-window.json"
printf 'DELTA: none' | python3 "$WW" --cycle 7 --app "$tmp2" >/dev/null 2>&1; rc=$?
chk "corrupt state => fail-closed exit 10" "[ '$rc' = '10' ]"

rm -rf "$tmp" "$tmp2"
echo
if [ "$fails" -ne 0 ]; then echo "$fails FAILURE(S)"; exit 1; fi
echo "ALL WIRING TESTS PASSED"
