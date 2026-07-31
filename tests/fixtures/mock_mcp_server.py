#!/usr/bin/env python3
"""Mock MCP stdio server for jcode-mcp-probe.py tests.

Speaks newline-delimited JSON-RPC: initialize, tools/list, tools/call.
Configured by env:
  MOCK_TOOLS        comma-separated tool names to report
  MOCK_CALL_ISERROR "1" -> tools/call result carries isError: true
  MOCK_CALL_TEXT    text of the first content block (default "base: AutoCo")
  MOCK_DIE          "1" -> exit immediately (unreachable-server case)
"""
import json
import os
import sys

if os.environ.get("MOCK_DIE") == "1":
    sys.exit(1)

tools = [t for t in os.environ.get("MOCK_TOOLS", "").split(",") if t]
call_text = os.environ.get("MOCK_CALL_TEXT", "base: AutoCo")
call_iserror = os.environ.get("MOCK_CALL_ISERROR") == "1"

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
    except json.JSONDecodeError:
        continue
    method = msg.get("method")
    rid = msg.get("id")
    if rid is None:
        continue  # notification
    if method == "initialize":
        result = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}},
                  "serverInfo": {"name": "mock", "version": "1"}}
    elif method == "tools/list":
        result = {"tools": [{"name": t, "inputSchema": {"type": "object"}}
                            for t in tools]}
    elif method == "tools/call":
        result = {"content": [{"type": "text", "text": call_text}]}
        if call_iserror:
            result["isError"] = True
    else:
        result = {}
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": rid, "result": result}) + "\n")
    sys.stdout.flush()
