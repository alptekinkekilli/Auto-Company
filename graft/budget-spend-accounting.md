---
name: Budget & spend accounting
slug: budget-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
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
sources_digest: 2cbe60ad78f30cad6a0df446408acc8f10b869265f715e536d53ddccc86f8d65
links:
  - to: cycle-orchestration-engine-routing
    relation: part_of
    description: >-
      The budget gates live inside auto-loop.sh and gate which engine runs each
      cycle.
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

Measures and enforces spend across engines. engine-usage-cost.py prices token streams with a --model-hint fallback for watchdog-killed cycles; auto-loop.sh's evaluate_budget_gates enforces 15 APP-263 gates with fail-closed ccusage reads that never lower a same-period prior observation; codex spend is summed from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER) rather than maxed.

## Related

- part of [[cycle-orchestration-engine-routing]] — The budget gates live inside auto-loop.sh and gate which engine runs each cycle.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
