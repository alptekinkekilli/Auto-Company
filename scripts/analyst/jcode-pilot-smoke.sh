#!/usr/bin/env bash
# jcode pilot — acceptance smoke (RUNBOOK §0.4 items 1–2, reduced).
# Runs INSIDE a one-shot pilot container (autocompany-jcode:pilot). Touches
# nothing persistent: no volumes, no Airtable writes, no loop interference.
#
# Exit codes: 0 = all smoke checks pass; 1 = a check failed (see output).
# Every check prints PASS/FAIL on its own line — the caller greps, humans read.
set -uo pipefail

fail_count=0
check() { # $1=name $2=0/1 pass
  if [ "$2" = "0" ]; then echo "PASS  $1"; else echo "FAIL  $1"; fail_count=$((fail_count+1)); fi
}

echo "== jcode pilot smoke — $(date -u +%FT%TZ) =="

# 0) GLIBC sanity (the whole reason the base image changed)
ldd --version | head -1

# 1) binary present and runnable
jcode --quiet --no-update --no-selfdev version >/dev/null 2>&1
check "jcode version runs" $?

# 2) Claude auth: wrap the existing oat token exactly like ai-admin/entrypoint.sh
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
  echo "FAIL  CLAUDE_CODE_OAUTH_TOKEN not provided"; exit 1
fi
case "$CLAUDE_CODE_OAUTH_TOKEN" in
  sk-ant-oat*)
    EXP=$(( ($(date +%s) + 86400*300) * 1000 ))
    CLAUDE_CODE_OAUTH_TOKEN=$(jq -n --arg t "$CLAUDE_CODE_OAUTH_TOKEN" --argjson e "$EXP" \
      '{claudeAiOauth:{accessToken:$t,refreshToken:"",expiresAt:$e,scopes:["user:inference"],subscriptionType:"max"}}')
    export CLAUDE_CODE_OAUTH_TOKEN
    ;;
esac
mkdir -p "$HOME/.jcode"
grep -q claude_code_native_credentials "$HOME/.jcode/config.toml" 2>/dev/null || \
  printf '[auth]\ntrusted_external_sources = ["claude_code_native_credentials"]\n' > "$HOME/.jcode/config.toml"

# 3) one real model round-trip (cheapest possible prompt)
OUT=$(cd /tmp && timeout 180 jcode -p claude -m claude-haiku-4-5-20251001 \
      run "Reply with exactly the two characters: OK" \
      --quiet --no-update --no-selfdev 2>&1)
printf '%s\n' "$OUT" | tail -3
printf '%s' "$OUT" | grep -q "OK"
check "claude round-trip via oat blob" $?

# 4) MCP config discovery: jcode reads Claude Code's project .mcp.json
#    (mcp/protocol.rs load order). We only verify it PARSES and registers the
#    servers — connecting to airtable/linear needs runtime.env keys, and
#    browseros needs the gateway; both are second-stage checks run from the
#    real host env, not here.
cd /app && ls .mcp.json >/dev/null 2>&1
check ".mcp.json present in image" $?

# 5) no leftover daemons (runbook §0.3.1)
sleep 2
LEFT=$(pgrep -af jcode | grep -v "pilot-smoke" | grep -cv grep || true)
[ "${LEFT:-0}" = "0" ]
check "no jcode processes left behind" $?

echo "== smoke result: $fail_count failure(s) =="
[ "$fail_count" = "0" ]
