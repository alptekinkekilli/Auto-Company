---
name: MCP configuration and probe
slug: mcp-configuration-and-probe
type: system
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/core/jcode-mcp-probe.py
    hash: 60fdd2addf2f53741d03e21002a00b6ee9d8895af1fae9746a51308e67672b67
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
  - path: tests/test_jcode_mcp_config.sh
    hash: d6e5f312040010b657623eed1bd3a7b2b30bdd004870c9dc69e0d63b4d4a5d33
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: afa9f21302723a41c39abcc3acf4623a8e8ceb14f436e7b26a863669b9b28ba1
links:
  - to: mcp-key-fallback
    relation: uses
    description: >-
      The generated config embeds the Keychain fallback command that the
      fallback test exercises.
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

Generation of .mcp.json wrapping HTTP MCP servers in the mcp-remote stdio bridge, and the deterministic probe that validates server manifests. Secrets never appear in argv (ps-readable) — the literal ${VAR} placeholder rides in --header while the real value lives in the env block. The generator refuses to write a partial config; the probe requires at least one proven readcheck per server and exact match of destructive tool lists.

## Related

- uses [[mcp-key-fallback]] — The generated config embeds the Keychain fallback command that the fallback test exercises.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
