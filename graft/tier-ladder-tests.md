---
name: Tier ladder tests
slug: tier-ladder-tests
type: system
sources:
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 53b1c709d020ad69894bd767f046b6a9adb7a7661c913e24209b19c3dbead38d
links:
  - to: auto-loop-core
    relation: validates
    description: Tests the apply_tier_ladder function extracted from auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

tests/test_tier_ladder_daily.sh extracts apply_tier_ladder() from auto-loop.sh via awk and runs it in a harness with mocked budget-gate env vars, covering eight scenarios: disabled ladder, unset budget, empty/full/mid spend, per-engine independence, MODEL_LABEL on Codex-routed cycles, and combined model:effort rung syntax. It sets budget-gate variables directly because the function only reads them, not computes them.

## Related

- validates [[auto-loop-core]] — Tests the apply_tier_ladder function extracted from auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
