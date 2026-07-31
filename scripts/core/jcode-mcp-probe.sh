#!/usr/bin/env bash
# RUNTIME proof that jcode can actually reach the required MCP servers.
#
#   jcode-mcp-probe.sh [required_csv]   (default: airtable,linear,context7,browseros)
#
# Why a runtime probe and not a config check: a config listing four servers proves
# nothing about four servers being reachable, and jcode reports NO ERROR for a server
# that fails to launch — the model just silently has fewer tools. Measured 2026-07-31:
# the community `airtable-mcp-server` package died on its own broken dependency
# (`Cannot find module 'hono/ws'`) and every check that read the config file passed
# while Airtable — this company's most-used write surface — was simply absent from the
# cycle. A boot check that cannot see that is decoration.
#
# So this asks jcode itself, once, and greps its answer.
#
# Exit: 0 all required servers present · 1 one or more missing · 2 the probe could not
# run (which is also a failure — an unprovable capability is not a capability).
set -uo pipefail

# `airtable-call-ok` is deliberately in the required set: a server can be VISIBLE and
# still fail every call — measured 2026-07-31, when the airtable bridge appeared in the
# model's server list and then answered "Failed to connect to MCP server 'airtable'" on
# each attempt (a corrupt npx dependency cache). Visibility is not capability, so the
# probe now proves one real read.
REQUIRED="${1:-${JCODE_MCP_REQUIRED:-airtable,linear,context7,browseros,airtable-call-ok}}"
JCODE_BIN="${JCODE_BIN:-$(command -v jcode 2>/dev/null || echo /usr/local/bin/jcode)}"
PROVIDER="${JCODE_PROBE_PROVIDER:-claude}"
MODEL="${JCODE_PROBE_MODEL:-claude-haiku-4-5}"
TIMEOUT="${JCODE_PROBE_TIMEOUT:-180}"
WORKDIR="${JCODE_PROBE_CWD:-${PROJECT_DIR:-/app}}"

[ -x "$JCODE_BIN" ] || { echo "MCP_PROBE_FAILED: jcode not executable at $JCODE_BIN" >&2; exit 2; }

# The loop deliberately keeps the RAW sk-ant-oat token in its own environment (so the
# CLI rollback path keeps working) and wraps it only inside each jcode subprocess. This
# probe is its own process, so it must do the same wrap — without it jcode gets a token
# shape it cannot use, answers nothing, and the probe reports "unreachable" for servers
# that are perfectly fine. (Exactly what happened on the first canary run.)
case "${CLAUDE_CODE_OAUTH_TOKEN:-}" in
    sk-ant-oat*)
        _exp=$(( ($(date +%s) + 86400*300) * 1000 ))
        _wrapped=$(python3 -c 'import json,os,sys; print(json.dumps({"claudeAiOauth":{"accessToken":os.environ["CLAUDE_CODE_OAUTH_TOKEN"],"refreshToken":"","expiresAt":int(sys.argv[1]),"scopes":["user:inference"],"subscriptionType":"max"}}))' "$_exp" 2>/dev/null || true)
        [ -n "$_wrapped" ] && export CLAUDE_CODE_OAUTH_TOKEN="$_wrapped"
        unset _wrapped _exp
        ;;
esac

ev="$(mktemp)"; trap 'rm -f "$ev"' EXIT

# Deliberately the cheapest model and a read-only question: this runs on every boot.
# --tools is NOT restricted here; the probe must see what the harness will see, and the
# cycle-time allowlist is applied separately by auto-loop.sh.
timeout "$TIMEOUT" "$JCODE_BIN" -p "$PROVIDER" -m "$MODEL" -C "$WORKDIR" \
    run 'Do TWO things. (1) Call the airtable MCP tool that lists bases and note whether the CALL SUCCEEDED. (2) Then reply with one line: the comma-separated lowercase names of every MCP server you can see, and append ",airtable-call-ok" only if the call in step 1 actually returned data. Nothing else.' \
    --quiet --no-update --no-selfdev --ndjson > "$ev" 2>/dev/null
rc=$?

answer=""
if [ -s "$ev" ] && [ -x "$(dirname "$0")/jcode-final-text.py" ]; then
    answer="$(python3 "$(dirname "$0")/jcode-final-text.py" "$ev" 2>/dev/null | tr '[:upper:]' '[:lower:]')"
fi

if [ -z "$answer" ]; then
    echo "MCP_PROBE_FAILED: no answer from jcode (rc=$rc) — cannot prove MCP reachability" >&2
    exit 2
fi

missing=""
for r in $(printf '%s' "$REQUIRED" | tr ',' ' '); do
    case "$answer" in *"$r"*) ;; *) missing="$missing $r" ;; esac
done

if [ -n "$missing" ]; then
    echo "MCP_PROBE_MISSING:$missing" >&2
    echo "  jcode answered: $(printf '%s' "$answer" | head -c 200)" >&2
    exit 1
fi

echo "MCP_PROBE_OK: $(printf '%s' "$answer" | head -c 200)"
exit 0
