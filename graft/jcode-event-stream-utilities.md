---
name: jcode Event Stream Utilities
slug: jcode-event-stream-utilities
type: system
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
sources_digest: 1f796fb69faf2ddb0e51c4f3628fc7ed30de13034f051e334e55704ca4197287
links:
  - to: cost-budget-ledger-adapters
    relation: part_of
    description: engine-usage-cost.py is the token-to-cost adapter for the budget ledger.
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
  - symbol: final_text
    kind: function
    at: 'scripts/core/jcode-final-text.py:L30-L48'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-final-text.py:L51-L61'
---
<!-- context:generated:start -->
## Summary

CLI utilities that consume jcode --ndjson event streams. jcode-final-text.py reconstructs the full assistant answer by concatenating all text_delta events and preferring the longer of deltas vs done.text (done.text can silently truncate on tool-using runs). engine-usage-cost.py (also here) sums all tokens events for cost. Both tolerate malformed lines and use only the standard library.

## Related

- part of [[cost-budget-ledger-adapters]] — engine-usage-cost.py is the token-to-cost adapter for the budget ledger.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
