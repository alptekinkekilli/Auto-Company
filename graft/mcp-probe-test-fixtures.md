---
name: MCP probe & test fixtures
slug: mcp-probe-test-fixtures
type: system
sources:
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
  - path: tests/test_browse_extract.sh
    hash: 37b269657d3077acf85e81540cd0355f9e97b432f0e6e1d973c2dfc170a887a6
sources_digest: 8768a5d08b7dac2f877ec71835de3f1487d1dd4ef20a6494b2b649037a913d22
links:
  - to: mcp-key-verification
    relation: validates
    description: >-
      The mock server stands in for real MCP servers that verify-mcp-keys.py
      checks.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Test infrastructure for MCP integration: mock_mcp_server.py is a deterministic stdio JSON-RPC 2.0 mock (configured via env vars MOCK_TOOLS/MOCK_CALL_TEXT/MOCK_CALL_ISERROR/MOCK_DIE) used to test jcode-mcp-probe.py, and browse-extract tests use an inline fake MCP gateway HTTP server to run offline. The mock ignores notifications, skips malformed JSON, and always returns a result even for unknown methods.

## Related

- validates [[mcp-key-verification]] — The mock server stands in for real MCP servers that verify-mcp-keys.py checks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
