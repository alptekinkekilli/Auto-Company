---
name: MCP key fallback
slug: mcp-key-fallback
type: concept
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 7e5496c29eae3646af4874f74f0d70e22230b762a74acdfb7e38e93197b41aca
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: 180b81c101d03061f68fb213f66f64bd3983edca109c0019c3e995995fdd477a
links:
  - to: mcp-config-sync-invariant
    relation: part_of
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

The .mcp.json config embeds a Keychain fallback that fires on macOS when a literal ${VAR} placeholder or unset variable arrives, but never inside the container where the `security` binary is absent. Secrets are placed in the server spec's env block (never argv) to avoid ps leaks; the generator refuses to write a partial config when a required variable is unset.

## Related

- part of [[mcp-config-sync-invariant]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
