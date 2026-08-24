---
name: Analyst Engine
slug: analyst-engine
type: system
sources:
  - path: tests/test_analyst_engine.sh
    hash: d4c762d2c85a4dbbeea39462739b8cb7a56b8f3cdcc4f88aa2ebbb4018d1f531
sources_digest: 3caff833918f15ba83b196b29e5fd07a3e9feb83c002de94bbf8fa3549432094
links:
  - to: auto-loop-core
    relation: uses
    description: Runs as a cycle engine alongside the main loop.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

opportunity-analyst-jcode.sh runs the analyst engine with provider-specific env vars and effort levels; fails closed without CLAUDE_CODE_OAUTH_TOKEN; done-event session_id lands deduplicated in analyst-jcode-sessions.log.

## Related

- uses [[auto-loop-core]] — Runs as a cycle engine alongside the main loop.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
