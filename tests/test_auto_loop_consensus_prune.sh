#!/usr/bin/env bash
# Wiring test for the consensus-prune hook inside auto-loop.sh (2026-10-08).
# Layer 1: static invariants; Layer 2: the helper behaves as the loop invokes it.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOOP="$REPO/scripts/core/auto-loop.sh"
CP="$REPO/scripts/ops/consensus-prune.py"
fails=0
pass() { printf 'PASS %s\n' "$1"; }
fail() { printf 'FAIL %s\n' "$1"; fails=$((fails+1)); }
chk()  { if eval "$2"; then pass "$1"; else fail "$1"; fi; }

# --- Layer 1: static wiring ---
chk "auto-loop.sh parses (bash -n)" "bash -n '$LOOP'"
chk "consensus-prune invoked post-cycle" "grep -qE 'consensus-prune.py. --cycle' '$LOOP'"
chk "capture set-e safe" "grep -qE '_cp_out=.\\(.*consensus-prune.py.*\\) \\|\\| true' '$LOOP'"
chk "gated on cycle_failed_reason empty" "grep -qF 'if [ -z \"\${cycle_failed_reason:-}\" ] && [ -f \"\$SCRIPT_DIR/../ops/consensus-prune.py\" ]' '$LOOP'"
chk "alarm line telegram-gated" "grep -qF \"grep -q 'CONSENSUS-PRUNE —'\" '$LOOP'"
lg=$(grep -n 'ledger-guard.py" --cycle' "$LOOP" | head -1 | cut -d: -f1)
cp=$(grep -n 'consensus-prune.py" --cycle' "$LOOP" | head -1 | cut -d: -f1)
chk "prune runs AFTER ledger-guard" "[ -n '$lg' ] && [ -n '$cp' ] && [ '$cp' -gt '$lg' ]"
chk "PROMPT-SIZE text: harness archives" "grep -qF 'the harness' '$LOOP' && grep -qF 'archives them automatically' '$LOOP'"
chk "PROMPT-SIZE text: model prune instruction removed" "! grep -qF 'prune resolved/stale' '$LOOP'"
chk "PROMPT-SIZE text: read IN FULL kept" "grep -qF 'IN FULL and treat its contents' '$LOOP'"
chk "prod-mechanism guard in sync" "python3 '$REPO/scripts/prod-mechanism-guard.py' --check-sync >/dev/null 2>&1"

# --- Layer 2: call-site contract ---
tmp="$(mktemp -d)"; mkdir -p "$tmp/memories" "$tmp/logs" "$tmp/docs/operations"
f="$tmp/memories/consensus.md"
printf '# Auto Company Consensus\n\n## Company State\nok\n\n## What We Did This Cycle\n\n' > "$f"
for n in $(seq 60 -1 21); do
  printf -- '- **Cycle %d — m.**\n' "$n" >> "$f"
  for _ in $(seq 1 30); do printf '  continuation %s\n' "$(printf 'x%.0s' $(seq 1 60))" >> "$f"; done
  printf '\n' >> "$f"
done
printf '## Next Action\n- go\n' >> "$f"
# v2 (2026-10-09): What We Did has a byte cap too; lift it so this KEEP=12 fixture still counts entries.
out="$(CONSENSUS_PRUNE_KEEP=12 CONSENSUS_PRUNE_CAP_WWD=1000000 python3 "$CP" --cycle 60 --app "$tmp" 2>/dev/null)"; rc=$?
chk "helper exit 0 + moved line" "[ '$rc' = '0' ] && printf '%s' \"$out\" | grep -q 'moved' && printf '%s' \"$out\" | grep -q 'docs/operations/consensus-archive-'"
chk "archive file exists" "ls '$tmp'/docs/operations/consensus-archive-*.md >/dev/null 2>&1"
chk "12 entries kept" "[ \"\$(grep -c '^- \\*\\*Cycle' '$f')\" = '12' ]"
chk "required markers intact" "grep -q '^# Auto Company Consensus' '$f' && grep -q '^## Next Action' '$f' && grep -q '^## Company State' '$f'"
out2="$(CONSENSUS_PRUNE_KEEP=12 CONSENSUS_PRUNE_CAP_WWD=1000000 python3 "$CP" --cycle 61 --app "$tmp" 2>/dev/null)"
chk "second run silent" "[ -z \"$out2\" ]"
rm -rf "$tmp"

echo
if [ "$fails" -ne 0 ]; then echo "$fails FAILURE(S)"; exit 1; fi
echo "ALL WIRING TESTS PASSED"
