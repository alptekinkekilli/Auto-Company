---
name: tier ladder daily tests
slug: tier-ladder-daily-tests
type: system
sources:
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 53b1c709d020ad69894bd767f046b6a9adb7a7661c913e24209b19c3dbead38d
links:
  - to: auto-loop-sh
    relation: validates
    description: Exercises apply_tier_ladder() tier selection.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash harness (tests/test_tier_ladder_daily.sh) that extracts apply_tier_ladder() via awk and runs eight scenarios with mocked budget-gate env vars (TOTAL_DAILY_BUDGET_USD, BG_CLAUDE_DAILY, BG_CODEX_DAILY) and tier ladder strings, covering disabled ladder, unset budget, empty/full/mid spend, per-engine independence, MODEL_LABEL on Codex-routed cycles, and combined model:effort rungs. Sets budget-gate variables directly because apply_tier_ladder() only reads them.

## Related

- validates [[auto-loop-sh]] — Exercises apply_tier_ladder() tier selection.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
