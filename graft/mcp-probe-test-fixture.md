---
name: MCP Probe Test Fixture
slug: mcp-probe-test-fixture
type: file
sources:
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
sources_digest: d41c2c418dd351366a8be5287cd5eda2e5b636c4f854c074f9b15af1153ce6e9
links:
  - to: mcp-key-verification
    relation: validates
    description: Used to test MCP server probing behavior
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A mock MCP stdio server used as a test fixture for jcode-mcp-probe.py, implementing minimal JSON-RPC 2.0 over newline-delimited stdin/stdout. Behavior configured entirely via env vars (MOCK_TOOLS, MOCK_CALL_TEXT, MOCK_CALL_ISERROR, MOCK_DIE). Ignores notifications, silently skips malformed JSON, always returns a result object even for unknown methods — a deterministic stand-in for a real MCP server.

## Related

- validates [[mcp-key-verification]] — Used to test MCP server probing behavior
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
