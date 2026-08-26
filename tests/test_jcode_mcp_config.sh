#!/usr/bin/env bash
# The jcode MCP config generator must never put a secret where `ps` can read it.
#
#   bash tests/test_jcode_mcp_config.sh
#
# Background. The generator wraps http servers in the mcp-remote stdio bridge and used to
# EXPAND ${VAR} header values straight into argv — the exact shape that leaked three API
# keys via `ps` on 2026-08-01, reproduced in the loop's own tool surface. mcp-remote
# documents (and we proved behaviourally on 2026-08-02, with a local HTTP sink receiving
# the real value while argv held the placeholder) that it expands ${VAR} in --header
# values from its own environment. So the contract pinned here is:
#
#   1. argv carries the LITERAL ${VAR} placeholder, never the secret
#   2. the secret rides in the server spec's env block, which probe and jcode pass through
#   3. a header referencing an UNSET variable skips the server (fail-closed, named)
#   4. --print masks both argv header values and env values — a diagnostic that leaks
#      is a diagnostic that gets pasted into a chat
#
# Overrides note: airtable/linear are FORCED to hosted endpoints by OVERRIDES, so the
# fixture uses a neutral server name that no override touches.
set -uo pipefail
cd "$(dirname "$0")/.."
GEN=scripts/core/jcode-mcp-config.py
fail=0
contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in output"; fail=1 ;; esac; }
not_contains() { case "$2" in *"$3"*) echo "  FAIL $1: secret '$3' leaked"; fail=1 ;; *) echo "  PASS $1" ;; esac; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT
SECRET_L="canary-linear-9f2kv"
SECRET_A="canary-airtable-7q1zx"

# A realistic mirror of production .mcp.json: all four REQUIRED servers, because the
# generator (correctly) refuses to write a partial config — the first fixture here had
# one server and never produced an output file at all.
cat > "$SB/src.json" <<'EOF'
{"mcpServers": {
  "context7": {"command": "sh", "args": ["-c", "exec npx -y @upstash/context7-mcp"],
               "env": {"CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"}},
  "airtable": {"command": "npx", "args": ["-y", "airtable-mcp-server"],
               "env": {"AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}"}},
  "linear":   {"command": "npx", "args": ["-y", "@tacticlaunch/mcp-linear"],
               "env": {"LINEAR_API_KEY": "${LINEAR_API_KEY}"}},
  "browseros": {"type": "http", "url": "http://172.17.0.1:9245/mcp"}
}}
EOF
# JCODE_MCP_SKIP="" turns OFF the OPREQ-A charter deny for airtable/linear so this test can
# still exercise their override + secret-masking code paths (live for the RFQ re-enable).
# The default-skip (airtable/linear absent) is covered by tests/test_mcp_config_manifest_sync.sh.
run_gen() { JCODE_MCP_SKIP="" LINEAR_API_KEY="$SECRET_L" AIRTABLE_API_KEY="$SECRET_A" CONTEXT7_API_KEY="ctx7sk-canary" \
    python3 "$GEN" --src "$SB/src.json" "$@"; }

echo "1. hosted-endpoint secrets stay out of argv, ride in env (linear+airtable overrides)"
run_gen --dest "$SB/out.json" >/dev/null 2>&1 || { echo "  FAIL generator rc"; fail=1; }
for pair in "linear LINEAR_API_KEY $SECRET_L" "airtable AIRTABLE_API_KEY $SECRET_A"; do
  set -- $pair; srv=$1; var=$2; sec=$3
  ARGS=$(python3 -c "import json;print(json.dumps(json.load(open('$SB/out.json'))['mcpServers']['$srv']['args']))")
  not_contains "$srv argv clean" "$ARGS" "$sec"
  contains "$srv argv keeps placeholder" "$ARGS" "Bearer \${$var}"
  ENVV=$(python3 -c "import json;print(json.load(open('$SB/out.json'))['mcpServers']['$srv'].get('env',{}).get('$var',''))")
  if [ "$ENVV" = "$sec" ]; then echo "  PASS $srv env carries the value"; else echo "  FAIL $srv env missing/wrong"; fail=1; fi
done

echo "2. unset variable -> server skipped and named, no partial config written"
# context7 is a REQUIRED server (linear/airtable left REQUIRED under OPREQ-A), so unset ITS
# var to trigger the partial-config refusal. JCODE_MCP_SKIP="" keeps the fixture's other
# servers in play so the only thing missing is the REQUIRED context7.
ERR=$(env -u CONTEXT7_API_KEY JCODE_MCP_SKIP="" LINEAR_API_KEY="$SECRET_L" AIRTABLE_API_KEY="$SECRET_A" \
    python3 "$GEN" --src "$SB/src.json" --dest "$SB/out2.json" 2>&1); RC=$?
contains "names the variable" "$ERR" "CONTEXT7_API_KEY"
contains "refuses partial" "$ERR" "refusing to write"
if [ ! -f "$SB/out2.json" ] && [ "$RC" -ne 0 ]; then echo "  PASS nothing written, non-zero"; else
  echo "  FAIL partial config written or rc=0"; fail=1; fi

echo "3. --print masks argv header values and env values"
P=$(run_gen --print 2>/dev/null)
not_contains "print clean of linear secret" "$P" "$SECRET_L"
not_contains "print clean of airtable secret" "$P" "$SECRET_A"
contains "env masked" "$P" '"LINEAR_API_KEY": "***"'

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
