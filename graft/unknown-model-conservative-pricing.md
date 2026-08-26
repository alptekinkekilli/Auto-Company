---
name: Unknown-Model Conservative Pricing
slug: unknown-model-conservative-pricing
type: concept
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: scripts/ops/cost-audit.py
    hash: f861b3352eb593e372a5a81bdaa068411ec3c7aa179e78df814b68dafffd08f7
sources_digest: 3d062de50babd97cf040d2e8d38711d783fb10f684271e5224a4305f17b4b1ab
links:
  - to: cost-budget-ledger-adapters
    relation: implements
    description: >-
      The pricing table and safety factor are implemented in
      engine-usage-cost.py.
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
  - symbol: utc_day
    kind: function
    at: 'scripts/ops/cost-audit.py:L42-L43'
  - symbol: read_ledger
    kind: function
    at: 'scripts/ops/cost-audit.py:L46-L67'
  - symbol: read_loop_log
    kind: function
    at: 'scripts/ops/cost-audit.py:L70-L111'
  - symbol: read_jcode_log
    kind: function
    at: 'scripts/ops/cost-audit.py:L114-L131'
  - symbol: read_tool_inventory
    kind: function
    at: 'scripts/ops/cost-audit.py:L134-L141'
  - symbol: fmt_money
    kind: function
    at: 'scripts/ops/cost-audit.py:L144-L145'
  - symbol: build_report
    kind: function
    at: 'scripts/ops/cost-audit.py:L148-L303'
  - symbol: main
    kind: function
    at: 'scripts/ops/cost-audit.py:L306-L324'
---
<!-- context:generated:start -->
## Summary

A cross-cutting safety invariant: unknown models are priced at the most expensive known row times a 5x safety factor and flagged estimated:true, so a budget gate never silently passes at zero cost. STRICT=1 makes unknown models exit 3 instead. The same conservative philosophy appears in cost-audit.py distinguishing calibrated from 'phantom' estimated costs.

## Related

- implements [[cost-budget-ledger-adapters]] — The pricing table and safety factor are implemented in engine-usage-cost.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
