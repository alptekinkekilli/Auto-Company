---
name: auto-loop
slug: auto-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 195d5132db1beb91938c913265df3bf517a0b676f6a8664523d3cdc5bffb0420
links:
  - to: set-e-shape-lint
    relation: validates
    description: auto-loop.sh is linted for the fatal set -e test-and-action pattern.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Core orchestration loop including apply_tier_ladder(), which selects a model tier from a daily budget with per-engine independence (one engine's spend doesn't affect the other's tier) and combined model:effort rung syntax. Reads budget-gate variables directly rather than computing them.

## Related

- validates [[set-e-shape-lint]] — auto-loop.sh is linted for the fatal set -e test-and-action pattern.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
