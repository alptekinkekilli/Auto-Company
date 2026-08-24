---
name: Budget and spend accounting
slug: budget-and-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
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
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 008461a9ddcf3ed9ece80cc6682d6d680e7da83e6cd67c877c1a8319da57f40c
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: These functions are extracted from auto-loop.sh and driven by the loop.
  - to: engine-cost-pricing
    relation: uses
    description: >-
      engine-usage-cost.py prices token streams; the model-hint flag prevents
      unknown-model fallback from inflating costs 5x.
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

The budget-gate, tier-ladder, and spend-accounting logic (APP-263) that enforces daily/weekly/5h caps, sums Codex spend from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER), and latches holds on degraded reads. Fail-closed: a first-ever ccusage failure latches a hold and returns NA, and degraded reads never overwrite a higher cached figure.

## Related

- part of [[auto-loop-core-engine]] — These functions are extracted from auto-loop.sh and driven by the loop.
- uses [[engine-cost-pricing]] — engine-usage-cost.py prices token streams; the model-hint flag prevents unknown-model fallback from inflating costs 5x.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
