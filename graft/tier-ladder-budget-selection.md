---
name: tier ladder budget selection
slug: tier-ladder-budget-selection
type: concept
sources:
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 53b1c709d020ad69894bd767f046b6a9adb7a7661c913e24209b19c3dbead38d
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: apply_tier_ladder() lives in auto-loop.sh
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

apply_tier_ladder() selects engine tier based on daily budget (APP-263). Per-engine independence: one engine's spend does not affect the other's tier. Supports MODEL_LABEL on Codex-routed cycles and combined model:effort rung syntax. Budget-gate variables are set directly because the function only reads them, not computes them.

## Related

- part of [[auto-loop-core-engine]] — apply_tier_ladder() lives in auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
