---
name: budget & spend accounting
slug: budget-spend-accounting
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
  - to: auto-loop-core-loop
    relation: part_of
    description: These functions live in auto-loop.sh and are invoked each cycle.
  - to: cycle-metadata-extraction
    relation: uses
    description: >-
      engine-usage-cost.py prices token streams; the model-hint must never
      override an actual completed model from the done event.
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

The spend-measurement and budget-gating subsystem: ccusage reads (fail-closed, never lowering a same-period prior), the TOTAL_SPEND_LEDGER rows written by jcode-harness cycles, daily/weekly/5h period resets, budget gates (APP-263), and the tier ladder that selects model/effort from remaining daily budget. Codex spend is summed from two disjoint sources (ccusage + ledger) rather than maxed, because maxing previously hid real spend.

## Related

- part of [[auto-loop-core-loop]] — These functions live in auto-loop.sh and are invoked each cycle.
- uses [[cycle-metadata-extraction]] — engine-usage-cost.py prices token streams; the model-hint must never override an actual completed model from the done event.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
