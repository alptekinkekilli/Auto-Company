---
name: MCP & Runtime Verification
slug: mcp-runtime-verification
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
sources_digest: 0dc077d291e00e181165c65ffec1f73d76c37a8e510bc1008570b6e1b86bbf55
links:
  - to: auto-loop-harness
    relation: validates
    description: >-
      verify-mcp-keys.py checks the loop process's environment after a deploy;
      context7-check.py audits cycles for missing documentation lookups.
generator:
  version: 1
covers:
  - symbol: externals
    kind: function
    at: 'scripts/ops/context7-check.py:L59-L75'
  - symbol: scan
    kind: function
    at: 'scripts/ops/context7-check.py:L78-L108'
  - symbol: walk_calls
    kind: function
    at: 'scripts/ops/context7-check.py:L111-L122'
  - symbol: verdict
    kind: function
    at: 'scripts/ops/context7-check.py:L125-L138'
  - symbol: main
    kind: function
    at: 'scripts/ops/context7-check.py:L141-L170'
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
---
<!-- context:generated:start -->
## Summary

Tooling that verifies MCP server configuration and runtime behavior. verify-mcp-keys.py inspects the environment of the running auto-loop.sh process via /proc/<pid>/environ (not its own shell, avoiding docker exec's fresh-shell which lacks entrypoint-sourced variables) to check each MCP server's key shape (Airtable keys contain a dot, Linear keys start with lin_api_, Context7 keys start with ctx7sk), never printing key values. context7-check.py audits cycles to ensure external library imports are accompanied by a Context7 documentation lookup, deliberately not firing on the project's own stdlib-only ops scripts to avoid false alarms. The mock MCP server fixture provides a deterministic stdio stand-in for integration tests.

## Related

- validates [[auto-loop-harness]] — verify-mcp-keys.py checks the loop process's environment after a deploy; context7-check.py audits cycles for missing documentation lookups.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
