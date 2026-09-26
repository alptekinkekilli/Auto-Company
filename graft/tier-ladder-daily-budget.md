---
name: tier ladder daily budget
slug: tier-ladder-daily-budget
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: e91c7fc83a0c89558b17f69dd7e478709e2929460a1505a5c549382b8b9ba4d6
links:
  - to: auto-loop-core-engine
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

apply_tier_ladder() selects engine tiers from daily budget gates (TOTAL_DAILY_BUDGET_USD, BG_CLAUDE_DAILY, BG_CODEX_DAILY) with per-engine independence and combined model:effort rung syntax; it only reads the budget-gate variables, never computes them.

## Related

- part of [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
