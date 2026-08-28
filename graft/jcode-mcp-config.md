---
name: jcode-mcp-config
slug: jcode-mcp-config
type: file
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 7e5496c29eae3646af4874f74f0d70e22230b762a74acdfb7e38e93197b41aca
sources_digest: afba053cdca71df3b543395426a11107a151fb274f9c6d864344b51808214c64
links:
  - to: jcode-mcp-probe
    relation: produces
    description: Generates the mcp.json config that the probe spawns servers from.
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
---
<!-- context:generated:start -->
## Summary

Generates ~/.jcode/mcp.json from project .mcp.json because jcode v0.64.2 ignores project config. Wraps HTTP/SSE servers in mcp-remote stdio bridge; stdio servers pass through unless skipped via JCODE_MCP_SKIP. Atomic write with freshness stamp (epoch+sha256) for boot probe. Secrets left unexpanded in argv to avoid ps leaks.

## Related

- produces [[jcode-mcp-probe]] — Generates the mcp.json config that the probe spawns servers from.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
