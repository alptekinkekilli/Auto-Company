#!/usr/bin/env bash
# The boot probe (jcode-mcp-probe.py rule 1) FAILS THE BOOT — crash-loops the container —
# if the generated loop config's server set != the manifest's server set. The mock-probe
# tests only exercise the probe LOGIC against fixtures; NOTHING checked the REAL files were
# in sync. This does: it runs the ACTUAL generator against the ACTUAL .mcp.json and compares
# to the ACTUAL jcode-mcp-manifest.json — so re-adding a server to one file but not the other
# (the OPREQ-A re-enable trap, and the exact class that crash-looped the loop once already)
# fails HERE instead of in production.
#
#   bash tests/test_mcp_config_manifest_sync.sh
set -uo pipefail
cd "$(dirname "$0")/.."

# CONTEXT7_API_KEY must be non-empty or convert() skips context7 (its env references it) —
# a local-only artifact that has nothing to do with server-set consistency. Give it a dummy;
# --print masks it anyway.
export CONTEXT7_API_KEY="${CONTEXT7_API_KEY:-ctx7sk-dummy-for-sync-test}"

python3 - <<'PY'
import json, subprocess, sys
gen = subprocess.run(
    ["python3", "scripts/core/jcode-mcp-config.py", "--src", ".mcp.json", "--print"],
    capture_output=True, text=True)
if gen.returncode != 0 or not gen.stdout.strip():
    print("FAIL: config generator did not print a config"); print(gen.stderr); sys.exit(1)
cfg = set(json.loads(gen.stdout)["mcpServers"].keys())
man = set(json.load(open("scripts/core/jcode-mcp-manifest.json"))["servers"].keys())
rc = json.load(open("scripts/core/jcode-mcp-manifest.json"))["readchecks"]
rc_servers = {r["server"] for r in rc}

fail = 0
def check(name, cond):
    global fail
    print(("  PASS " if cond else "  FAIL ")+name); fail = fail or (0 if cond else 1)

check(f"config servers == manifest servers ({sorted(cfg)} vs {sorted(man)})", cfg == man)
# every non-exempt manifest server must have a readcheck (the manifest's own rule)
exempt = {n for n, s in json.load(open("scripts/core/jcode-mcp-manifest.json"))["servers"].items()
          if "readcheck_exempt" in s}
need_rc = man - exempt
check(f"every non-exempt server has a readcheck (need {sorted(need_rc)}, have {sorted(rc_servers)})",
      need_rc <= rc_servers)
# OPREQ-A invariant: airtable+linear are NOT in the loop config during the charter
check("airtable denied from loop config (OPREQ-A)", "airtable" not in cfg)
check("linear denied from loop config (OPREQ-A)", "linear" not in cfg)

sys.exit(1 if fail else 0)
PY
rc=$?
echo
[ "$rc" = 0 ] && echo "ALL PASS" || echo "FAILURES"
exit "$rc"
