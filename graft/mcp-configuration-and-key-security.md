---
name: MCP configuration and key security
slug: mcp-configuration-and-key-security
type: system
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
sources_digest: fcf0d0d48a051a6279048bea4f9375980ce1af0efd39595aa45762320f391057
links:
  - to: mcp-probe
    relation: produces
    description: >-
      jcode-mcp-config.py generates the config that jcode-mcp-probe.py
      validates.
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
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
---
<!-- context:generated:start -->
## Summary

Generation and verification of the .mcp.json MCP server config: jcode-mcp-config.py wraps HTTP servers in mcp-remote stdio bridges, keeping secrets in env (never argv), with a macOS Keychain fallback that must never fire inside the container. verify-mcp-keys.py checks deployed keys via /proc environ.

## Related

- produces [[mcp-probe]] — jcode-mcp-config.py generates the config that jcode-mcp-probe.py validates.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
