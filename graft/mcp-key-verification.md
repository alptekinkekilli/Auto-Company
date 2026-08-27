---
name: MCP key verification
slug: mcp-key-verification
type: system
sources:
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
sources_digest: 53579789209d19207ea77c4e9195c8f1f5f66496648a6b53cdcedba956c4bec7
links:
  - to: mcp-configuration-probe
    relation: validates
    description: Verifies the deployed keys match the shape predicates the config expects.
generator:
  version: 1
covers:
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
---
<!-- context:generated:start -->
## Summary

verify-mcp-keys.py checks each MCP server receives a well-formed key after deploy by reading the running loop's /proc/<pid>/environ (not a fresh shell), never printing key values.

## Related

- validates [[mcp-configuration-probe]] — Verifies the deployed keys match the shape predicates the config expects.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
