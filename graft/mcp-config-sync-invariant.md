---
name: MCP config sync invariant
slug: mcp-config-sync-invariant
type: concept
sources:
  - path: tests/test_mcp_config_manifest_sync.sh
    hash: 372a198973bc97e73dd00c1acafe2fe458887504be2f5ef9849242d6549c1112
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: e36b83fc83b19f37b90da6ed99de2b014d0fbd39beb6704514026a9dfce4fca6
links:
  - to: auto-loop-core-engine
    relation: configures
    description: The preflight list in auto-loop.sh must agree with the manifest
  - to: mcp-config-generator
    relation: validates
    description: The generator's output is compared against the manifest
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The generated loop MCP config's mcpServers set must stay in sync with the manifest (scripts/core/jcode-mcp-manifest.json) and the hardcoded JCODE_MCP_CONFIG_REQUIRED preflight list in auto-loop.sh; divergence causes a boot crash-loop. airtable and linear must be absent from the loop config (OPREQ-A invariant), and every non-exempt manifest server needs a proven readcheck. A dedicated test runs the real generator and compares all three pins.

## Related

- configures [[auto-loop-core-engine]] — The preflight list in auto-loop.sh must agree with the manifest
- validates [[mcp-config-generator]] — The generator's output is compared against the manifest
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
