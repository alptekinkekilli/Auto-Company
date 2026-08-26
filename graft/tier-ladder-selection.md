---
name: tier ladder selection
slug: tier-ladder-selection
type: concept
sources:
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 53b1c709d020ad69894bd767f046b6a9adb7a7661c913e24209b19c3dbead38d
links:
  - to: core-bash-scripts
    relation: part_of
    description: The function is defined in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

apply_tier_ladder() in auto-loop.sh picks a model tier from a daily-budget ladder (APP-263). It only reads budget-gate variables (TOTAL_DAILY_BUDGET_USD, BG_CLAUDE_DAILY, BG_CODEX_DAILY) rather than computing them, supports per-engine independence (one engine's spend doesn't affect the other's tier), MODEL_LABEL on Codex-routed cycles, and combined model:effort rung syntax. Tests extract the function via awk and mock the env vars directly.

## Related

- part of [[core-bash-scripts]] — The function is defined in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
