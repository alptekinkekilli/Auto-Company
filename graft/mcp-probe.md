---
name: MCP probe
slug: mcp-probe
type: file
sources:
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: 30360d88aad0bab433575ab05149700a3fb89604ae38e77b068196f3a5916ae8
links:
  - to: mcp-config-generator
    relation: validates
    description: Probe validates the generated config's server/tool sets
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/core/jcode-mcp-probe.py deterministically validates MCP server configs against a mock stdio server with no model/network. It requires at least one proven readcheck per server (with an exemption mechanism for servers like browseros), enforces the manifest's destructive tool list exactly matches live tools, and checks the denylist covers both base and per-server tool names. 13 scenarios cover exact-match, missing/extra servers, destructive-tool gaps, readcheck failures, and exemptions.

## Related

- validates [[mcp-config-generator]] — Probe validates the generated config's server/tool sets
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
