---
name: Engine usage cost adapter (engine-usage-cost)
slug: engine-usage-cost-adapter-engine-usage-cost
type: file
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
sources_digest: 6ee6a7bfcdad67740cc3e9c82b68d36bdd80cf963fef48f593806b0c3ca5a41c
links:
  - to: budget-calibration-cost-audit
    relation: produces
    description: >-
      Feeds cost_usd into the APP-263 budget ledger consumed by
      budget-calibration-report.py and cost-audit.py.
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

Converts token-usage data into notional USD costs at Anthropic list prices so the APP-263 budget ledger can consume jcode's token-only output. Sums ALL tokens events (not just done.usage, which undercounts multi-tool cycles), prices unknown models at the most expensive known row times 5x safety factor flagged estimated:true (STRICT=1 exits 3 instead), and honors TTL-specific cache breakdowns. --model-hint never overrides a real done event but prevents a killed cycle from being priced at the inflated unknown-model rate.

## Related

- produces [[budget-calibration-cost-audit]] — Feeds cost_usd into the APP-263 budget ledger consumed by budget-calibration-report.py and cost-audit.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
