---
name: MCP config generation & boot probe
slug: mcp-config-generation-boot-probe
type: system
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 7e5496c29eae3646af4874f74f0d70e22230b762a74acdfb7e38e93197b41aca
  - path: scripts/core/jcode-mcp-probe.py
    hash: 60fdd2addf2f53741d03e21002a00b6ee9d8895af1fae9746a51308e67672b67
sources_digest: 5c486cb9b9e24ea7acf023003a03ae50970460766baf723ea3eb1774622a9ed8
links:
  - to: context7-compliance-checker
    relation: validates
    description: >-
      context7-check.py inspects cycle ndjson logs to detect code importing
      external libraries without first calling Context7, complementing the boot
      probe.
generator:
  version: 1
covers:
  - symbol: expand
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L96-L108'
  - symbol: sub
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L100-L105'
  - symbol: convert
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L111-L162'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L165-L276'
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

Two stdlib-only components that make jcode's MCP layer deterministic and verifiable. jcode-mcp-config.py generates ~/.jcode/mcp.json from project .mcp.json (jcode v0.64.2 ignores project config), wrapping HTTP/SSE servers in mcp-remote stdio bridge, applying hard-coded overrides for linear/airtable hosted endpoints, leaving secrets unexpanded in argv to avoid ps leaks, and stamping freshness (epoch+sha256). jcode-mcp-probe.py is a deterministic boot probe that spawns each server and speaks JSON-RPC 2.0 over stdio, enforcing five fail-closed gates (exact server-set match, handshake within timeout, destructive tools exactly matching manifest, JCODE_TOOLS_DENY coverage, readcheck with no protocol error). A documented gotcha: tools/list alone proved insufficient — Context7 passed boot for days while never being called, so a real read call is now mandatory.

## Related

- validates [[context7-compliance-checker]] — context7-check.py inspects cycle ndjson logs to detect code importing external libraries without first calling Context7, complementing the boot probe.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
