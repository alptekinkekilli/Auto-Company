---
name: MCP key fallback
slug: mcp-key-fallback
type: system
sources:
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: 0c0222525a7f47e855e3eae01f1df1201123dd2371c32c6c36c82e8cfcd267e2
links:
  - to: mcp-configuration-probe
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The .mcp.json embedded command that falls back to macOS Keychain via the security binary when a ${VAR} placeholder or unset variable is seen, but never fires inside the container where security is absent. Keys are placed in ENV not argv to avoid ps leaks.

## Related

- part of [[mcp-configuration-probe]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
