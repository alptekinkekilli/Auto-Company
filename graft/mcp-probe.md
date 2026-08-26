---
name: MCP probe
slug: mcp-probe
type: system
sources:
  - path: scripts/core/jcode-mcp-probe.py
    hash: 60fdd2addf2f53741d03e21002a00b6ee9d8895af1fae9746a51308e67672b67
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
sources_digest: 4e5805e69edce8229dc6c4c2fb5cd20a312a17b3d2789496ee247d6fa0f8f398
links:
  - to: mcp-configuration-and-key-security
    relation: uses
    description: Probe reads the .mcp.json config and manifest to validate servers.
generator:
  version: 1
covers:
  - symbol: ServerError
    kind: class
    at: 'scripts/core/jcode-mcp-probe.py:L43-L44'
  - symbol: StdioClient
    kind: class
    at: 'scripts/core/jcode-mcp-probe.py:L47-L155'
  - symbol: __init__
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L50-L65'
  - symbol: _remaining
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L67-L71'
  - symbol: _send
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L73-L79'
  - symbol: _read_msg
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L81-L102'
  - symbol: request
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L104-L116'
  - symbol: notify
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L118-L119'
  - symbol: initialize
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L121-L127'
  - symbol: list_tools
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L129-L137'
  - symbol: call_tool
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L139-L140'
  - symbol: close
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L142-L155'
  - symbol: probe_server
    kind: function
    at: 'scripts/core/jcode-mcp-probe.py:L158-L168'
  - symbol: judge_readcheck
    kind: function
    at: 'scripts/core/jcode-mcp-probe.py:L171-L186'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-probe.py:L189-L362'
---
<!-- context:generated:start -->
## Summary

Deterministic pre-cycle probe (jcode-mcp-probe.py) that validates each MCP server's tools against a manifest, requiring at least one proven readcheck per server and exact match of destructive tools, with a denylist covering base and per-server tools.

## Related

- uses [[mcp-configuration-and-key-security]] — Probe reads the .mcp.json config and manifest to validate servers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
