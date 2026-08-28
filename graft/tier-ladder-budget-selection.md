---
name: tier ladder budget selection
slug: tier-ladder-budget-selection
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 17b55034781a7a612d62c4dbd67aada347fa75067a70365aa442c44d730e0fe5
links:
  - to: auto-loop-sh-core-loop
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily-budget-based tier selection (APP-263) reading TOTAL_DAILY_BUDGET_USD and per-engine spend; engines are independent (one's spend doesn't affect the other's tier), supports model:effort rung syntax and MODEL_LABEL on Codex-routed cycles.

## Related

- part of [[auto-loop-sh-core-loop]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
