---
name: Tier ladder selection
slug: tier-ladder-selection
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 824da56e05c877fc937fe9fe5a8d42086dd21df51868365fe37d84abb6a39531
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
