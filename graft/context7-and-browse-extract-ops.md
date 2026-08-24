---
name: Context7 and browse-extract ops
slug: context7-and-browse-extract-ops
type: system
sources:
  - path: scripts/ops/browse-extract.py
    hash: ec67b37ee0a24df3eb9d5b06f16e7172c456153e7c7b8bd61edc2b54f7543aa1
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: tests/test_browse_extract.sh
    hash: 37b269657d3077acf85e81540cd0355f9e97b432f0e6e1d973c2dfc170a887a6
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
sources_digest: 802d81510972c0d0fd959ca2ab6ddd50f92e6754b02c9d69a815737bfb4fca43
links:
  - to: mcp-configuration-and-probe
    relation: uses
    description: browse-extract talks to the browseros MCP server over the gateway.
generator:
  version: 1
covers:
  - symbol: Gateway
    kind: class
    at: 'scripts/ops/browse-extract.py:L45-L83'
  - symbol: __init__
    kind: method
    at: 'scripts/ops/browse-extract.py:L46-L49'
  - symbol: post
    kind: method
    at: 'scripts/ops/browse-extract.py:L51-L67'
  - symbol: call
    kind: method
    at: 'scripts/ops/browse-extract.py:L69-L77'
  - symbol: handshake
    kind: method
    at: 'scripts/ops/browse-extract.py:L79-L83'
  - symbol: clip
    kind: function
    at: 'scripts/ops/browse-extract.py:L86-L91'
  - symbol: extract
    kind: function
    at: 'scripts/ops/browse-extract.py:L94-L119'
  - symbol: ToolError
    kind: class
    at: 'scripts/ops/browse-extract.py:L122-L123'
  - symbol: main
    kind: function
    at: 'scripts/ops/browse-extract.py:L126-L201'
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
---
<!-- context:generated:start -->
## Summary

context7-check.py audits cycles to ensure external library imports are accompanied by a Context7 documentation lookup (must not fire on the project's own stdlib-only ops scripts), and browse-extract.py greps/reads browser tabs via the MCP gateway, always closing the tab even on error paths.

## Related

- uses [[mcp-configuration-and-probe]] — browse-extract talks to the browseros MCP server over the gateway.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
