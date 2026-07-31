#!/usr/bin/env bash
# REVISE-2 gates B8-B10: the deterministic MCP probe against a mock stdio server.
#
#   bash tests/test_mcp_probe.sh
#
# Every verdict here comes from protocol-level facts produced by
# tests/fixtures/mock_mcp_server.py — no model, no network.
set -uo pipefail
cd "$(dirname "$0")/.."
PROBE=scripts/core/jcode-mcp-probe.py
MOCK="$(pwd)/tests/fixtures/mock_mcp_server.py"
fail=0
check_rc() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1: expected rc=$3 got rc=$2"; fail=1; fi; }
check_contains() { case "$2" in *"$3"*) echo "  PASS $1" ;; *) echo "  FAIL $1: '$3' not in output"; fail=1 ;; esac; }

SB="$(mktemp -d)"; trap 'rm -rf "$SB"' EXIT

AT_TOOLS="list_bases,list_records_for_table,delete_records_for_table,revert_action"
LN_TOOLS="get_issue,save_issue,delete_comment"
DENY_OK="mcp,gmail,mcp__at__delete_records_for_table,mcp__at__revert_action,mcp__ln__delete_comment"

write_config() { # $1 at-env  $2 ln-env  (K=V pairs separated by '|' — values may hold commas)
    python3 - "$SB" "$MOCK" "$1" "$2" <<'PY'
import json, sys
sb, mock, at_env, ln_env = sys.argv[1:5]
def env(spec):
    d = {}
    for kv in spec.split("|"):
        if "=" in kv:
            k, v = kv.split("=", 1); d[k] = v
    return d
cfg = {"mcpServers": {
    "at": {"command": "python3", "args": [mock], "env": env(at_env)},
    "ln": {"command": "python3", "args": [mock], "env": env(ln_env)},
}}
json.dump(cfg, open(sb + "/mcp.json", "w"))
PY
}

write_manifest() { # $1 at-destructive-json  $2 base-denied-json
    python3 - "$SB" "$1" "$2" <<'PY'
import json, sys
sb, at_d, base = sys.argv[1:4]
man = {
    "readcheck": {"server": "at", "tool": "list_bases", "arguments": {}},
    "base_denied": json.loads(base),
    "servers": {
        "at": {"destructive": json.loads(at_d)},
        "ln": {"destructive": ["delete_comment"]},
    },
}
json.dump(man, open(sb + "/manifest.json", "w"))
PY
}

run_probe() {
    JCODE_TOOLS_DENY="${DENY:-$DENY_OK}" python3 "$PROBE" \
        --config "$SB/mcp.json" --manifest "$SB/manifest.json" \
        --evidence "$SB/evidence.json" --timeout 20 2>&1
    echo "rc=$?"
}

echo "--- 1: exact match end-to-end -> OK, evidence written ---"
write_config "MOCK_TOOLS=$AT_TOOLS" "MOCK_TOOLS=$LN_TOOLS"
write_manifest '["delete_records_for_table","revert_action"]' '["mcp","gmail"]'
out="$(run_probe)"
check_contains "probe ok"   "$out" "MCP_PROBE_OK"
check_contains "readcheck ok" "$out" "readcheck=at:list_bases:ok"
check_contains "rc 0"       "$out" "rc=0"
check_contains "evidence has tool census" "$(cat "$SB/evidence.json")" '"tool_count": 4'
check_contains "evidence readcheck ok"    "$(cat "$SB/evidence.json")" '"ok": true'

echo "--- 2: server missing from config -> fail ---"
python3 -c 'import json,sys; c=json.load(open(sys.argv[1])); del c["mcpServers"]["ln"]; json.dump(c,open(sys.argv[1],"w"))' "$SB/mcp.json"
out="$(run_probe)"
check_contains "missing named" "$out" "config missing server(s): ln"
check_contains "rc 1"          "$out" "rc=1"

echo "--- 3: EXTRA server in config -> fail ---"
write_config "MOCK_TOOLS=$AT_TOOLS" "MOCK_TOOLS=$LN_TOOLS"
python3 -c 'import json,sys; c=json.load(open(sys.argv[1])); c["mcpServers"]["rogue"]={"command":"python3","args":[]}; json.dump(c,open(sys.argv[1],"w"))' "$SB/mcp.json"
out="$(run_probe)"
check_contains "extra named" "$out" "EXTRA server(s) not in the manifest: rogue"
check_contains "rc 1"        "$out" "rc=1"

echo "--- 4: live destructive tool the manifest does not expect -> fail ---"
write_config "MOCK_TOOLS=$AT_TOOLS,drop_everything|X=1" "MOCK_TOOLS=$LN_TOOLS"
write_manifest '["delete_records_for_table","revert_action"]' '["mcp","gmail"]'
out="$(run_probe)"
check_contains "extra destructive named" "$out" "does not expect: drop_everything"
check_contains "rc 1"                    "$out" "rc=1"

echo "--- 5: manifest destructive tool ABSENT live (stale manifest) -> fail ---"
write_config "MOCK_TOOLS=list_bases,revert_action" "MOCK_TOOLS=$LN_TOOLS"
out="$(run_probe)"
check_contains "missing destructive named" "$out" "MISSING expected destructive tool(s): delete_records_for_table"
check_contains "rc 1"                      "$out" "rc=1"

echo "--- 6: denylist gap -> fail even when servers are healthy ---"
write_config "MOCK_TOOLS=$AT_TOOLS" "MOCK_TOOLS=$LN_TOOLS"
out="$(DENY="mcp,gmail,mcp__at__delete_records_for_table,mcp__at__revert_action" run_probe)"
check_contains "gap named" "$out" "denylist missing 'mcp__ln__delete_comment'"
check_contains "rc 1"      "$out" "rc=1"
out="$(DENY="gmail,mcp__at__delete_records_for_table,mcp__at__revert_action,mcp__ln__delete_comment" run_probe)"
check_contains "base mcp tool gap named" "$out" "denylist missing base tool 'mcp'"

echo "--- 7: readcheck isError=true -> fail (protocol-level, not prose) ---"
write_config "MOCK_TOOLS=$AT_TOOLS|MOCK_CALL_ISERROR=1" "MOCK_TOOLS=$LN_TOOLS"
out="$(run_probe)"
check_contains "isError named" "$out" "readcheck at:list_bases failed: isError=true"
check_contains "rc 1"          "$out" "rc=1"

echo "--- 8: readcheck output BEGINNING with an error string -> fail ---"
write_config "MOCK_TOOLS=$AT_TOOLS|MOCK_CALL_TEXT=Error: unauthorized" "MOCK_TOOLS=$LN_TOOLS"
out="$(run_probe)"
check_contains "error text named" "$out" "content begins with an error string"
check_contains "rc 1"             "$out" "rc=1"

echo "--- 9: server process dies -> unreachable, fail ---"
write_config "MOCK_TOOLS=$AT_TOOLS|MOCK_DIE=1" "MOCK_TOOLS=$LN_TOOLS"
out="$(run_probe)"
check_contains "unreachable named" "$out" "server 'at' unreachable"
check_contains "rc 1"              "$out" "rc=1"

echo "--- 10: manifest without a readcheck -> fail (a read must be proven) ---"
write_config "MOCK_TOOLS=$AT_TOOLS" "MOCK_TOOLS=$LN_TOOLS"
python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); del m["readcheck"]; json.dump(m,open(sys.argv[1],"w"))' "$SB/manifest.json"
out="$(run_probe)"
check_contains "no-readcheck named" "$out" "manifest defines no readcheck"
check_contains "rc 1"               "$out" "rc=1"

echo
[ "$fail" -eq 0 ] && echo "ALL MCP-PROBE TESTS PASS" || { echo "FAILURES PRESENT"; exit 1; }
