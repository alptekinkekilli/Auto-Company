---
name: Budget & spend accounting
slug: budget-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 4ba21a832fa11b0f4dbfa7c4e8bbecd298e8777319651934a2af5294d31665ce
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: These functions live in auto-loop.sh and gate cycle execution.
  - to: engine-usage-cost-model
    relation: uses
    description: >-
      engine-usage-cost.py prices token streams; the model-hint behavior
      interacts with budget accounting.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The spend-measurement and gating machinery in auto-loop.sh: ccusage reads (fail-closed, never lowering a same-period prior), the TOTAL_SPEND_LEDGER rows from jcode-harness cycles, 5h/daily/weekly period resets, budget holds, and the discretionary daily cap. Spend is summed from two disjoint sources (ccusage + ledger) rather than maxed, because maxing previously hid real spend.

## Related

- part of [[auto-loop-core-engine]] — These functions live in auto-loop.sh and gate cycle execution.
- uses [[engine-usage-cost-model]] — engine-usage-cost.py prices token streams; the model-hint behavior interacts with budget accounting.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
