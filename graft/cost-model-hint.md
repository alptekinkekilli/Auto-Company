---
name: Cost model hint
slug: cost-model-hint
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
sources_digest: 09399485c2e8e9c57d25cea9e3e3d4e9c22b720c86c8238a7c7a4b25e1fc5140
links:
  - to: budget-gates
    relation: uses
    description: Feeds the spend figures the budget gates enforce.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The pricing of token streams from the engine, with a --model-hint flag that applies a real tariff when a watchdog-killed cycle produced token events but no done event. The invariant: a hint must never override an actual completed model's model field, or the model-substitution guard would be defeated. Without a hint or done event, it falls back to the conservative unknown-model row with estimated: true.

## Related

- uses [[budget-gates]] — Feeds the spend figures the budget gates enforce.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
