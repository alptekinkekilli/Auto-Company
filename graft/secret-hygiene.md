---
name: Secret hygiene
slug: secret-hygiene
type: concept
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
sources_digest: fcf0d0d48a051a6279048bea4f9375980ce1af0efd39595aa45762320f391057
links:
  - to: mcp-configuration-and-key-security
    relation: implements
    description: The config generator and key verifier enforce this invariant.
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

Secrets never appear in argv (ps-readable) or in diagnostics: MCP keys ride in env blocks with ${VAR} placeholders in argv, verify-mcp-keys prints only lengths, and --print masks values as ***.

## Related

- implements [[mcp-configuration-and-key-security]] — The config generator and key verifier enforce this invariant.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
