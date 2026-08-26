#!/usr/bin/env bash
# Regression tests for APP-240: extract_cycle_metadata() killed the loop (and so
# the container) on every Codex-routed cycle.
#
#   bash tests/test_cycle_metadata.sh scripts/core/auto-loop.sh
#
# Reproduces the exact failing conditions under the same `set -euo pipefail`
# the real script runs with, so a regression here fails loudly instead of
# silently taking production down.
set -uo pipefail
SRC="${1:-scripts/core/auto-loop.sh}"
fail=0
check() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected '$3' got '$2'"; fail=1; fi; }

run_case() {  # <engine> <override> <fallback> <result_message>
    bash -c '
        set -euo pipefail
        ENGINE="$1"; CYCLE_ENGINE_OVERRIDE="$2"; FALLBACK_USED="$3"
        RESULT_MESSAGE="$4"; OUTPUT="raw output"; EXIT_CODE=0
        '"$(awk '/^_cycle_ran_on_codex\(\)/,/^}/' "$SRC")"'
        '"$(awk '/^extract_cycle_metadata\(\)/,/^}/' "$SRC")"'
        extract_cycle_metadata
        printf "%s|%s|%s" "$CYCLE_TYPE" "$CYCLE_SUBTYPE" "${RESULT_TEXT:0:20}"
    ' _ "$1" "$2" "$3" "$4" 2>&1
    echo "|rc=$?"
}

# Codex's final message is plain prose — no line starts with `{`. This is the
# exact input that used to kill the loop.
CODEX_MSG='Cycle complete. I reviewed the tender packet and updated consensus.'
CLAUDE_MSG='Ignoring 3 permissions.allow entries
{"type":"result","subtype":"success","total_cost_usd":1.23,"result":"did the thing"}'

echo "--- 1: alternation-routed Codex cycle (ENGINE=claude, override=codex) — THE CRASH ---"
out=$(run_case claude codex 0 "$CODEX_MSG")
check "does not die" "${out##*|}" "rc=0"
check "typed as codex" "$(printf '%s' "$out" | cut -d'|' -f1)" "codex_exec"

echo "--- 2: usage-limit fallback to Codex (FALLBACK_USED=1) ---"
out=$(run_case claude "" 1 "$CODEX_MSG")
check "does not die" "${out##*|}" "rc=0"
check "typed as codex" "$(printf '%s' "$out" | cut -d'|' -f1)" "codex_exec"

echo "--- 3: Codex as primary engine (was always fine, must stay fine) ---"
out=$(run_case codex "" 0 "$CODEX_MSG")
check "does not die" "${out##*|}" "rc=0"
check "typed as codex" "$(printf '%s' "$out" | cut -d'|' -f1)" "codex_exec"

echo "--- 4: normal Claude cycle still parses its JSON ---"
out=$(run_case claude "" 0 "$CLAUDE_MSG")
check "does not die" "${out##*|}" "rc=0"
check "subtype from JSON" "$(printf '%s' "$out" | cut -d'|' -f2)" "success"

echo "--- 5: Claude cycle with NO JSON at all (warnings only) must not die either ---"
out=$(run_case claude "" 0 "Ignoring 3 permissions.allow entries")
check "does not die" "${out##*|}" "rc=0"

echo "--- 6: codex-final-text.py turns the raw --json -o event stream into clean SUMMARY text ---"
# Regression for the Codex-CLI SUMMARY leak: the -o message file is a JSONL event stream
# (thread.started / item.completed{agent_message} / turn.completed), not plain text.
# run_codex_cycle_cli now pipes it through this extractor before it becomes RESULT_MESSAGE.
EXTRACTOR="$(dirname "$SRC")/codex-final-text.py"
NDJSON="$(mktemp)"
printf '%s\n' \
  '{"type":"thread.started","thread_id":"01a03e14"}' \
  '{"type":"turn.started"}' \
  '{"type":"item.completed","item":{"id":"item_0","type":"reasoning","text":"internal thinking, must be ignored"}}' \
  '{"type":"item.completed","item":{"id":"item_1","type":"agent_message","text":"Cycle complete. Updated consensus."}}' \
  '{"type":"turn.completed","usage":{"input_tokens":10}}' > "$NDJSON"
got=$(python3 "$EXTRACTOR" "$NDJSON")
check "extracts agent_message text" "$got" "Cycle complete. Updated consensus."
check "does NOT leak thread.started" "$(printf '%s' "$got" | grep -c 'thread.started' || true)" "0"
check "does NOT leak reasoning text" "$(printf '%s' "$got" | grep -c 'internal thinking' || true)" "0"
# plain-text / non-JSON -o (older CLI or parse failure) -> empty, so the caller falls back to raw
printf 'plain final message, not a json stream\n' > "$NDJSON"
python3 "$EXTRACTOR" "$NDJSON" >/dev/null; rc=$?
check "empty extraction exits 1 (fallback path fires)" "$rc" "1"
rm -f "$NDJSON"

echo; [ "$fail" = 0 ] && echo "ALL PASS" || { echo "FAILURES"; exit 1; }
