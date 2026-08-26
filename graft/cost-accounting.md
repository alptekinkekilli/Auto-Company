---
name: Cost Accounting
slug: cost-accounting
type: concept
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
sources_digest: 6ee6a7bfcdad67740cc3e9c82b68d36bdd80cf963fef48f593806b0c3ca5a41c
links:
  - to: autonomous-loop
    relation: uses
    description: Feeds the loop's budget/spend accounting.
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

Converts token usage into notional USD at Anthropic list prices, an adapter so the APP-263 budget ledger can consume jcode's token-only output. Sums ALL tokens events (not just done.usage, which undercounts multi-tool cycles); unknown models priced at most-expensive-known × 5x safety factor flagged estimated:true, with STRICT=1 exiting 3. Conservative unknown-model pricing avoids silent zero-cost budget gates.

## Related

- uses [[autonomous-loop]] — Feeds the loop's budget/spend accounting.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
