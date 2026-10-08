---
name: MCP & Tooling Verification
slug: mcp-tooling-verification
type: system
sources:
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
sources_digest: 57b335385305c0fa3319e1138b99b4f1e0f67c78040445ae393ff0732d828f7f
links:
  - to: auto-loop-harness
    relation: validates
    description: >-
      verify-mcp-keys checks MCP server keys after a deploy by inspecting the
      loop process environment.
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

Verification and test-fixture tooling around MCP servers and tooling: verify-mcp-keys.py checks each MCP server's API key shape by reading the running auto-loop.sh process environment via /proc (avoiding docker exec's fresh-shell false failures), and mock_mcp_server.py is a deterministic stdio JSON-RPC fixture for jcode-mcp-probe integration tests.

## Related

- validates [[auto-loop-harness]] — verify-mcp-keys checks MCP server keys after a deploy by inspecting the loop process environment.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
