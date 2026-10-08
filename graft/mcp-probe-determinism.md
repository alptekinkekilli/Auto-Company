---
name: MCP probe determinism
slug: mcp-probe-determinism
type: concept
sources:
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: 30360d88aad0bab433575ab05149700a3fb89604ae38e77b068196f3a5916ae8
links:
  - to: mcp-configuration-and-manifest-sync
    relation: part_of
    description: jcode-mcp-probe.py implements the probe
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The deterministic MCP probe validates live servers against the manifest: exact-match success, missing/extra servers, unexpected or missing destructive tools, denylist gaps, readcheck failures (isError, error-prefixed content, server death), missing readchecks, and readcheck exemptions. At least one proven readcheck per server is required (with an exemption mechanism for servers like browseros); the manifest's destructive tool list must exactly match live tools; the denylist covers both base tools and per-server tool names.

## Related

- part of [[mcp-configuration-and-manifest-sync]] — jcode-mcp-probe.py implements the probe
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
