---
name: Budget gates
slug: budget-gates
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
sources_digest: 09399485c2e8e9c57d25cea9e3e3d4e9c22b720c86c8238a7c7a4b25e1fc5140
links:
  - to: auto-loop-harness
    relation: part_of
    description: evaluate_budget_gates and record_total_spend live in auto-loop.sh.
  - to: cost-model-hint
    relation: uses
    description: >-
      engine-usage-cost.py prices token streams; the --model-hint flag must
      never override an actual completed model.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 15 budget-gate behaviors mandated by APP-263 (2026-07-30): engine-specific gates, rollover independence, daily/weekly resets, duplicate run_id dedup, analyst session exclusion, stale-fallback, deterministic alternate routing. Spend is summed from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER) rather than maxed, because max previously caused real spend to vanish. Degraded reads never lower a same-period prior observation.

## Related

- part of [[auto-loop-harness]] — evaluate_budget_gates and record_total_spend live in auto-loop.sh.
- uses [[cost-model-hint]] — engine-usage-cost.py prices token streams; the --model-hint flag must never override an actual completed model.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
