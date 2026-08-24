---
name: Cost accounting adapter
slug: cost-accounting-adapter
type: file
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
sources_digest: 6ee6a7bfcdad67740cc3e9c82b68d36bdd80cf963fef48f593806b0c3ca5a41c
links:
  - to: autonomous-loop
    relation: uses
    description: Feeds the budget ledger consumed by the loop's spend gates.
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

Converts token usage to notional USD at Anthropic list prices for the budget ledger. Sums all tokens events (not just done.usage) from jcode ndjson; prices unknown models at 5x most-expensive with estimated flag; STRICT=1 exits 3 on unknown models.

## Related

- uses [[autonomous-loop]] — Feeds the budget ledger consumed by the loop's spend gates.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
