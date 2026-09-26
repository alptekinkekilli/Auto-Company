---
name: MCP config sync invariant
slug: mcp-config-sync-invariant
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: scripts/core/jcode-mcp-config.py
    hash: 7e5496c29eae3646af4874f74f0d70e22230b762a74acdfb7e38e93197b41aca
  - path: tests/test_mcp_config_manifest_sync.sh
    hash: 372a198973bc97e73dd00c1acafe2fe458887504be2f5ef9849242d6549c1112
sources_digest: 07dbd38727fb615ddd5ff2078c8f0a6a6d8bfb8f1efef98bbea9a113ceeb0732
links:
  - to: mcp-key-fallback
    relation: depends_on
  - to: mcp-probe
    relation: depends_on
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

The generated loop config's mcpServers set must stay in sync with the manifest and the hardcoded JCODE_MCP_CONFIG_REQUIRED preflight list, or the boot crash-loops; every non-exempt manifest server needs a readcheck, and airtable/linear must be absent from the loop config (OPREQ-A).

## Related

- depends on [[mcp-key-fallback]]
- depends on [[mcp-probe]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
