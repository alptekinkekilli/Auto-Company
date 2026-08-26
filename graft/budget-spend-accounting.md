---
name: Budget & spend accounting
slug: budget-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 421e004c7ebef884343c055f034507cca24c256dfb630c31ad2350e2e210068a
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: These functions live in auto-loop.sh and are extracted by tests via awk.
  - to: cycle-metadata-extraction
    relation: uses
    description: record_total_spend attributes each cycle's cost under its own run_id.
generator:
  version: 1
covers:
  - symbol: _n
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L66-L69'
  - symbol: cost_for
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L72-L110'
  - symbol: main
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L113-L191'
---
<!-- context:generated:start -->
## Summary

The spend-measurement and gating layer: sums Codex spend from two disjoint sources (ccusage CLI session files plus TOTAL_SPEND_LEDGER rows from jcode-harness cycles), applies 5h/daily/weekly budget gates, and latches holds on degraded reads. It is fail-closed: a first-ever ccusage failure latches a hold and returns NA, and degraded reads never lower a same-period prior observation.

## Related

- part of [[auto-loop-core-engine]] — These functions live in auto-loop.sh and are extracted by tests via awk.
- uses [[cycle-metadata-extraction]] — record_total_spend attributes each cycle's cost under its own run_id.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
