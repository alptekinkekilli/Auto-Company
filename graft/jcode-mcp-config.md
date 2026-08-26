---
name: jcode MCP Config
slug: jcode-mcp-config
type: file
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
sources_digest: 792fdcf7760d8d94c3ce71fa9b668595eb9fb46b5c0e0e63d43779960ca93a56
links: []
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
---
<!-- context:generated:start -->
## Summary

Generates global MCP config for the jcode harness; referenced by the entrypoint (which disables memory features when the harness is jcode) and by the jcode analyst runner. A documented gotcha: as of jcode v0.64.2 the tool does NOT read the project's .mcp.json, so smoke tests only verify the file parses and registers servers — actual connections are deferred to host-side checks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
