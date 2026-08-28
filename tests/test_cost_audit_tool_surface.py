#!/usr/bin/env python3
"""cost-audit §5 tool-surface: the 'advertised' column must reflect --disabled-tools.

WHY: the raw MCP schema-cache lists every tool a server advertises, but jcode HIDES the
JCODE_TOOLS_DENY subset from the real prompt prefix. Counting the raw cache made the
Program Auditor (2026-08-28 §8) re-raise OPREQ-1 ("17 never-called tools still advertised")
on tools that were already trimmed. §5 now subtracts the loop-hidden set, so a loop-hidden
tool is never a trim candidate.

  python3 tests/test_cost_audit_tool_surface.py
"""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("ca", os.path.join(ROOT, "scripts", "ops", "cost-audit.py"))
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)

fail = 0


def ok(m):
    print(f"  PASS {m}")


def no(m):
    global fail
    print(f"  FAIL {m}")
    fail = 1


# 1) read_disabled_tools parses the auto-loop.sh default (single source of truth).
#    Guards against the loop default silently dropping the OPREQ-1 trim.
os.environ.pop("JCODE_TOOLS_DENY", None)
denied = ca.read_disabled_tools(ROOT)
bro = {t for t in denied if "browseros" in t}
ctx = {t for t in denied if "context7" in t}
(ok if len(bro) == 15 else no)(f"browseros deny count = 15 (got {len(bro)})")
(ok if len(ctx) == 2 else no)(f"context7 deny count = 2 (got {len(ctx)})")
(ok if "mcp__browseros__tabs" not in denied else no)("browseros core (tabs) NOT denied")

# 2) env override wins over the auto-loop default.
os.environ["JCODE_TOOLS_DENY"] = "mcp__browseros__screenshot,foo"
d2 = ca.read_disabled_tools(ROOT)
(ok if d2 == {"mcp__browseros__screenshot", "foo"} else no)(f"env override wins (got {sorted(d2)})")
os.environ.pop("JCODE_TOOLS_DENY", None)

# 3) The §5 hidden/in-prefix arithmetic: a loop-hidden tool leaves the prefix.
#    Simulate browseros' 23-tool inventory (short names) against the real deny set.
inv = ["tab_groups", "diff", "download", "upload", "screenshot", "pdf", "windows", "run",
       "connector_mcp_servers", "discover_server_categories_or_actions", "get_category_actions",
       "get_action_details", "execute_action", "search_documentation", "handle_auth_failure",
       "tabs", "navigate", "snapshot", "act", "read", "grep", "wait", "evaluate"]
hidden = sum(1 for nm in inv if denied & {nm, f"mcp__browseros__{nm}"})
in_prefix = len(inv) - hidden
(ok if hidden == 15 else no)(f"browseros loop-hidden = 15 (got {hidden})")
(ok if in_prefix == 8 else no)(f"browseros in-prefix = 8 (got {in_prefix})")

# 4) Full-name inventory (namespaced) matches too — robustness to cache format.
inv_full = [f"mcp__browseros__{nm}" for nm in inv]
hidden_full = sum(1 for nm in inv_full if denied & {nm, f"mcp__browseros__{nm}"})
(ok if hidden_full == 15 else no)(f"namespaced inventory also hides 15 (got {hidden_full})")

print("ALL PASS" if fail == 0 else "FAILURES")
sys.exit(fail)
