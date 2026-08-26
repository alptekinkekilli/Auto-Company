---
name: Secret hygiene in argv vs env
slug: secret-hygiene-in-argv-vs-env
type: concept
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
  - path: tests/test_jcode_mcp_config.sh
    hash: d6e5f312040010b657623eed1bd3a7b2b30bdd004870c9dc69e0d63b4d4a5d33
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: f4b51100d4fed3e014b04787f04bde6c8985e59a8c4a6eecde27dcfa95b80fb7
links:
  - to: mcp-configuration-key-security
    relation: implements
    description: The argv/env split and masking are implemented in jcode-mcp-config.py.
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

A security invariant across the MCP stack: secrets must never appear in argv (where ps could read them) or in diagnostics that get pasted into chat. Literal ${VAR} placeholders ride in --header argv while real values live in env blocks; --print masks both as '***'; keys are placed in ENV rather than argv to avoid leaking via ps.

## Related

- implements [[mcp-configuration-key-security]] — The argv/env split and masking are implemented in jcode-mcp-config.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
