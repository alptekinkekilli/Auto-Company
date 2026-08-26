---
name: Fail-closed measurement invariant
slug: fail-closed-measurement-invariant
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 098fdc15d9f9370ea3817993e2a46a09eba1d6490d360bb652fafd5cfba8eb68
links:
  - to: budget-spend-accounting
    relation: implements
    description: >-
      The fail-closed behavior is implemented in _codex_spend_since and
      evaluate_budget_gates.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A cross-cutting invariant: any measurement that gates spend or budget must fail closed — a first-ever ccusage failure latches a hold and returns NA (not 0), degraded reads never lower a same-period prior observation, and unmeasured/zero-cost cycles fail and latch. This prevents silent spend under-reporting from defeating budget gates.

## Related

- implements [[budget-spend-accounting]] — The fail-closed behavior is implemented in _codex_spend_since and evaluate_budget_gates.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
