---
name: MCP key verification
slug: mcp-key-verification
type: file
sources:
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
sources_digest: 53579789209d19207ea77c4e9195c8f1f5f66496648a6b53cdcedba956c4bec7
links:
  - to: auto-loop-harness-budget-governance
    relation: validates
    description: Verifies the loop's MCP servers are correctly keyed after a deploy.
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

verify-mcp-keys.py checks that each MCP server (Airtable, Linear, Context7) receives a well-formed API key after deploy by inspecting /proc/<pid>/environ of the running auto-loop.sh process rather than its own shell environment — avoiding docker exec's fresh-shell environment which lacks entrypoint-sourced variables and caused false failures. Never prints key values, only lengths and shape status; detects macOS security wrappers; fails on absent/malformed keys.

## Related

- validates [[auto-loop-harness-budget-governance]] — Verifies the loop's MCP servers are correctly keyed after a deploy.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
