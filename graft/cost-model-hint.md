---
name: Cost Model Hint
slug: cost-model-hint
type: system
sources:
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
sources_digest: 7afc86ccc7eae6f8ebe4bb686a81caa44d50be47b23abca036d8985e85ae897b
links:
  - to: engine-adapters
    relation: part_of
    description: Pricing adapter used by engine cycles.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

engine-usage-cost.py prices token streams from the engine, with a --model-hint flag for watchdog-killed cycles that produce token events but no done event. A hint never overrides an actual completed model's model field, or the model-substitution guard would be defeated.

## Related

- part of [[engine-adapters]] — Pricing adapter used by engine cycles.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
