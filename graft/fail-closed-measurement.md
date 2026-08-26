---
name: Fail-closed measurement
slug: fail-closed-measurement
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 8047ae1ceb7eac76beba89e0584912e2500baee4f68bb2f372c872739a2c7193
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
sources_digest: 13d154d4aaa858742fe10527399fdf67b5eda29ac3ba12d3e7fed0e639dccadb
links:
  - to: budget-and-spend-accounting
    relation: implements
    description: >-
      Budget gates latch holds on degraded reads and never overwrite cache with
      lower figures.
generator:
  version: 1
covers:
  - symbol: file_sha16
    kind: function
    at: 'scripts/ops/state-snapshot.py:L54-L61'
  - symbol: directive_state
    kind: function
    at: 'scripts/ops/state-snapshot.py:L64-L72'
  - symbol: opreq_open
    kind: function
    at: 'scripts/ops/state-snapshot.py:L75-L87'
  - symbol: wowcar_sources
    kind: function
    at: 'scripts/ops/state-snapshot.py:L90-L104'
  - symbol: main
    kind: function
    at: 'scripts/ops/state-snapshot.py:L107-L166'
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
---
<!-- context:generated:start -->
## Summary

A cross-cutting invariant: degraded or missing measurements (ccusage, budget, snapshot, MCP keys) must fail closed or preserve prior observations, never silently lower a figure or park the company. Applies to budget gates, idle detection, and key verification.

## Related

- implements [[budget-and-spend-accounting]] — Budget gates latch holds on degraded reads and never overwrite cache with lower figures.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
