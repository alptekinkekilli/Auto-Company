---
name: Tier ladder selection
slug: tier-ladder-selection
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: e2254c052a9a09ae5e7b4ea291f115e745a1de6cb8568f6af3a808db2e06b150
links:
  - to: auto-loop-sh-core-loop
    relation: validates
    description: >-
      test_tier_ladder_daily.sh extracts apply_tier_ladder() and runs eight
      budget scenarios.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

apply_tier_ladder() picks a model tier from the daily budget and per-engine daily spend (BG_CLAUDE_DAILY, BG_CODEX_DAILY), with per-engine independence and combined model:effort rung syntax. It only reads budget-gate variables, never computes them, so tests set them directly.

## Related

- validates [[auto-loop-sh-core-loop]] — test_tier_ladder_daily.sh extracts apply_tier_ladder() and runs eight budget scenarios.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
