---
name: Budget & spend accounting
slug: budget-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
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
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
sources_digest: ae43b2ca9722918c376650b2c4964790adade3571a86989aa169e50991ded214
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Functions extracted from auto-loop.sh
  - to: state-snapshot-probe
    relation: uses
    description: 'idle detection reads DELTA: none from the snapshot'
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

The spend-measurement and gating subsystem: sums Codex spend from two disjoint sources (ccusage CLI sessions + TOTAL_SPEND_LEDGER rows), applies 5h/daily/weekly budget gates, and latches holds on degraded reads. Fail-closed: a first-ever ccusage failure latches a hold and returns NA, and degraded reads never lower a same-period prior observation.

## Related

- part of [[auto-loop-core-engine]] — Functions extracted from auto-loop.sh
- uses [[state-snapshot-probe]] — idle detection reads DELTA: none from the snapshot
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
