---
name: MCP boot & config generation
slug: mcp-boot-config-generation
type: system
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/core/jcode-mcp-probe.py
    hash: 60fdd2addf2f53741d03e21002a00b6ee9d8895af1fae9746a51308e67672b67
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
sources_digest: 25e5b115257e521f78f7ce4c017495308aefca86986825f521f62a663e14ff0c
links:
  - to: cost-budget-reporting
    relation: produces
    description: >-
      cost-audit reads the advertised-vs-called MCP tool surface from
      mcp-schema-cache.json.
  - to: jcode-event-stream-utilities
    relation: produces
    description: >-
      The generated mcp.json and probe evidence are consumed by the jcode log
      parsers.
generator:
  version: 1
covers:
  - symbol: expand
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L82-L94'
  - symbol: sub
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L86-L91'
  - symbol: convert
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L97-L148'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L151-L258'
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
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
---
<!-- context:generated:start -->
## Summary

Generates jcode's MCP server config from a project-local .mcp.json (wrapping HTTP/SSE servers in mcp-remote stdio bridges), then deterministically probes every server over JSON-RPC 2.0 with fail-closed gates (exact server-set match, handshake timeout, destructive-tool denylist coverage, mandatory read-only readcheck). The probe exists because tools/list alone proved insufficient — a server passed boot for days while never being called.

## Related

- produces [[cost-budget-reporting]] — cost-audit reads the advertised-vs-called MCP tool surface from mcp-schema-cache.json.
- produces [[jcode-event-stream-utilities]] — The generated mcp.json and probe evidence are consumed by the jcode log parsers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
