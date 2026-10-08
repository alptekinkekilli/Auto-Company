---
name: cost model hint
slug: cost-model-hint
type: concept
sources:
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
sources_digest: 7afc86ccc7eae6f8ebe4bb686a81caa44d50be47b23abca036d8985e85ae897b
links:
  - to: cost-audit-tool-surface
    relation: uses
    description: Both price token streams from the engine
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The --model-hint flag in engine-usage-cost.py prices token streams when a watchdog-killed cycle produces token events but no done event, preventing fallback to the unknown-model row (which previously inflated costs by 5× and suppressed the effort ladder). A valid hint applies the real tariff but still flags estimated: true and records basis as 'requested-model HINT'; an unrecognized hint is ignored; when a done event exists its model field wins and the hint is completely ignored. A hint must never override an actual completed model, or the model-substitution guard would be defeated.

## Related

- uses [[cost-audit-tool-surface]] — Both price token streams from the engine
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
