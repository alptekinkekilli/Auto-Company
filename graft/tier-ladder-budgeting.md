---
name: tier ladder budgeting
slug: tier-ladder-budgeting
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 06b251fba00767ca2de5410f64f6d561a37964fccc96cb904f5f4ee878fe358e
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: apply_tier_ladder() lives in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

apply_tier_ladder() (APP-263) selects engine tiers from daily budget spend, with per-engine independence (one engine's spend doesn't affect the other's tier), MODEL_LABEL on Codex-routed cycles, and combined model:effort rung syntax. It only reads budget-gate variables, never computes them.

## Related

- part of [[auto-loop-core-engine]] — apply_tier_ladder() lives in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
