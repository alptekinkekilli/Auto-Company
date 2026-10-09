---
name: Budget Gates and Spend Accounting
slug: budget-gates-and-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
sources_digest: 3d35c111515e4a59b1ee2359373bf79bb0171c839b4ec15c85cadb3d78c1239b
links:
  - to: auto-loop-harness-brakes-and-guards
    relation: part_of
    description: Budget gates are the money backstop for the work-window and bloat brakes
  - to: cycle-cost-and-turn-economics
    relation: uses
    description: Consumes cost measurements to enforce period caps
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The fail-closed budget enforcement in auto-loop.sh: evaluate_budget_gates and select_cycle_engine apply 15 APP-263-mandated behaviors (engine-specific gates, rollover independence, daily/weekly resets, duplicate run_id dedup, analyst session exclusion, stale-fallback). ccusage measurement is fail-closed — degraded reads never lower a same-period prior observation and latch a hold returning NA not 0. Codex spend is summed from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER rows) rather than taking the max, which previously caused real spend to vanish.

## Related

- part of [[auto-loop-harness-brakes-and-guards]] — Budget gates are the money backstop for the work-window and bloat brakes
- uses [[cycle-cost-and-turn-economics]] — Consumes cost measurements to enforce period caps
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
