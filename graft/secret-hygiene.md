---
name: Secret hygiene
slug: secret-hygiene
type: concept
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
  - path: tests/test_jcode_mcp_config.sh
    hash: d6e5f312040010b657623eed1bd3a7b2b30bdd004870c9dc69e0d63b4d4a5d33
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: 40fbea09d23e3097f52f64426f3fe99090b162b67b179d6bdef7fb5ae712c800
links:
  - to: mcp-configuration-and-probe
    relation: implements
    description: The generator enforces the placeholder-in-argv / value-in-env split.
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
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L19-L23'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L26-L63'
---
<!-- context:generated:start -->
## Summary

The invariant that secrets never appear in argv (ps-readable) or in diagnostics that could be pasted into a chat. Keys ride as literal ${VAR} placeholders in argv while real values live in env blocks; --print masks both; session-brief never writes secrets.

## Related

- implements [[mcp-configuration-and-probe]] — The generator enforces the placeholder-in-argv / value-in-env split.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
