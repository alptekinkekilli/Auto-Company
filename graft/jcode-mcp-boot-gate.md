---
name: jcode MCP boot gate
slug: jcode-mcp-boot-gate
type: system
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/core/jcode-mcp-probe.py
    hash: 60fdd2addf2f53741d03e21002a00b6ee9d8895af1fae9746a51308e67672b67
sources_digest: 08ef3aeec09c4abd5b3e13c38ac773d38ada0fe3af77376e33065837618b8333
links:
  - to: jcode-event-stream-utilities
    relation: produces
    description: >-
      The probe's StdioClient and config generation define the mcp.json and
      event-stream shapes that the audit scripts parse.
  - to: operator-escalation-gate
    relation: uses
    description: >-
      The probe's evidence JSON and exit codes feed the canary audit that
      operator_request_notify's audit log records.
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
---
<!-- context:generated:start -->
## Summary

Deterministic boot-time verification of MCP servers: generates the mcp.json config from a project-local .mcp.json (wrapping HTTP/SSE servers in mcp-remote stdio bridges), then probes each server over newline-delimited JSON-RPC 2.0 with a fail-closed gate set (exact server-set match, handshake timeout, destructive-tool census, denylist coverage, and a mandatory read-only tools/call). Replaces a model-based check that let Context7 pass boot for days while never being called. Writes atomic evidence JSON for the canary audit.

## Related

- produces [[jcode-event-stream-utilities]] — The probe's StdioClient and config generation define the mcp.json and event-stream shapes that the audit scripts parse.
- uses [[operator-escalation-gate]] — The probe's evidence JSON and exit codes feed the canary audit that operator_request_notify's audit log records.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
