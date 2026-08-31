#!/usr/bin/env bash
# Wiring test for the OPREQ-3 bloat brake + ledger-integrity guard inside auto-loop.sh.
# Layer 1: static invariants (a future edit that breaks the wiring fails here).
# Layer 2: call-site contract (the helpers, invoked as the loop invokes them, behave).
# Note: grep patterns use `.` where the source has a closing `"` after `.py`, to avoid
# embedding a literal quote inside the chk wrapper.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOOP="$REPO/scripts/core/auto-loop.sh"
LG="$REPO/scripts/ops/ledger-guard.py"
TB="$REPO/scripts/ops/turn-bloat-brake.py"
fails=0
pass() { printf 'PASS %s\n' "$1"; }
fail() { printf 'FAIL %s\n' "$1"; fails=$((fails+1)); }
chk()  { if eval "$2"; then pass "$1"; else fail "$1"; fi; }

# --- Layer 1: static wiring ---
chk "auto-loop.sh parses (bash -n)" "bash -n '$LOOP'"
chk "ledger-guard invoked post-cycle" "grep -qE 'ledger-guard.py. --cycle' '$LOOP'"
chk "ledger-guard capture set-e safe" "grep -qE '_lg_alarm=.\\(.*ledger-guard.py.*\\) \\|\\| true' '$LOOP'"
chk "ledger alarm telegram-gated" "grep -qF 'if [ -n \"\$_lg_alarm\" ] && [ -n \"\${TELEGRAM_BOT_TOKEN' '$LOOP'"
chk "turn-bloat --record with verdict" "grep -qE 'turn-bloat-brake.py. --record --cycle .* --verdict' '$LOOP'"
chk "turn-bloat --feedback hardens line" "grep -qE '_tb_hard=.\\(.*turn-bloat-brake.py. --feedback' '$LOOP'"
chk "turn-bloat feedback assigned to _turnfb_line" "grep -qF '_turnfb_line=\"\$_tb_hard\"' '$LOOP'"
chk "turn-bloat capture set-e safe" "grep -qE 'turn-bloat-brake.py. --feedback.*\\) \\|\\| true' '$LOOP'"

# --- Layer 2: call-site contract ---
tmp="$(mktemp -d)"; mkdir -p "$tmp/docs/operations" "$tmp/memories" "$tmp/logs"
L="$tmp/docs/operations/wowcar-gate0-source-of-truth-and-conflict-ledger-test.md"
mk() { : > "$1"; for i in $(seq 1 "$2"); do printf '## %d. s\nx\n\n' "$i" >> "$1"; done; }

mk "$L" 10
out="$(python3 "$LG" --cycle 1 --app "$tmp" 2>/dev/null)"; rc=$?
chk "ledger-guard first run exit 0 + silent" "[ '$rc' = '0' ] && [ -z \"$out\" ]"
chk "ledger-guard made a backup" "ls '$tmp'/logs/state-backups/1-* >/dev/null 2>&1"
mk "$L" 6
out="$(python3 "$LG" --cycle 2 --app "$tmp" 2>/dev/null)"
chk "ledger-guard alarms on section drop" "printf '%s' \"$out\" | grep -q 'LEDGER-GUARD'"

tb="$(mktemp -d)"; mkdir -p "$tb/logs"
python3 "$TB" --record --cycle 1 --verdict BLOATED --app "$tb" >/dev/null 2>&1
python3 "$TB" --record --cycle 2 --verdict BLOATED --app "$tb" >/dev/null 2>&1
out="$(python3 "$TB" --record --cycle 3 --verdict BLOATED --app "$tb" 2>/dev/null)"
chk "turn-bloat alarms on 3rd consecutive BLOATED" "printf '%s' \"$out\" | grep -q 'TURN-BLOAT'"
chk "turn-bloat feedback active during streak" "python3 '$TB' --feedback --app '$tb' 2>/dev/null | grep -q 'HARD BRAKE'"
python3 "$TB" --record --cycle 4 --verdict ok --app "$tb" >/dev/null 2>&1
chk "turn-bloat feedback cleared after ok" "[ -z \"$(python3 '$TB' --feedback --app '$tb' 2>/dev/null)\" ]"

rm -rf "$tmp" "$tb"
echo
if [ "$fails" -ne 0 ]; then echo "$fails FAILURE(S)"; exit 1; fi
echo "ALL WIRING TESTS PASSED"
