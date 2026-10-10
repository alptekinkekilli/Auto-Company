---
name: MCP probe
slug: mcp-probe
type: file
sources:
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: 30360d88aad0bab433575ab05149700a3fb89604ae38e77b068196f3a5916ae8
links:
  - to: mcp-config-generation-and-manifest-sync
    relation: validates
    description: Probe validates generated config against manifest
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

jcode-mcp-probe.py deterministically validates MCP server config against a manifest: exact-match success, missing/extra servers, unexpected/missing destructive tools, denylist gaps, readcheck failures, and readcheck exemptions. Requires at least one proven readcheck per server (with exemption for browseros), enforces the manifest's destructive tool list exactly matches live tools, and checks the denylist covers both base and per-server tool names.

## Related

- validates [[mcp-config-generation-and-manifest-sync]] — Probe validates generated config against manifest
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
