---
name: Engine usage cost model
slug: engine-usage-cost-model
type: file
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
sources_digest: a2b1bd124cd7ba74dd31158bdb8c9a13eb57a4917ac2311a98c871d74b0f03bc
links:
  - to: budget-spend-accounting
    relation: produces
    description: Priced token streams feed the budget gates.
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

engine-usage-cost.py prices token streams from the engine, with a --model-hint flag that applies a real tariff when a watchdog-killed cycle produced token events but no done event. A hint must never override an actual completed model (the model-substitution guard), and an unrecognized hint falls back to the conservative unknown-model row.

## Related

- produces [[budget-spend-accounting]] — Priced token streams feed the budget gates.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
