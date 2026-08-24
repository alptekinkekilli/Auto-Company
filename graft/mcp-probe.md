---
name: MCP Probe
slug: mcp-probe
type: system
sources:
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: 55559e8980b6126104d7b33c4e78709bbf95de3c057c135a2c2f2488aff7567f
links:
  - to: mcp-configuration
    relation: validates
    description: Probes the generated .mcp.json config against the manifest.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

jcode-mcp-probe.py deterministically validates MCP servers against a manifest: exact-match success, destructive-tool denylist coverage, and at least one proven readcheck per server (with exemptions like browseros). Tested against a mock stdio server.

## Related

- validates [[mcp-configuration]] — Probes the generated .mcp.json config against the manifest.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
