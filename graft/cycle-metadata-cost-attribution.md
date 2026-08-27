---
name: Cycle metadata & cost attribution
slug: cycle-metadata-cost-attribution
type: system
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: b5ed82199ad3a157d9d367a9826cbfb32bd35dc726e8ce2e4da5d7431306a8fe
links:
  - to: auto-loop-core-engine
    relation: part_of
  - to: budget-spend-accounting
    relation: produces
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
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

Extraction and pricing of per-cycle metadata and cost from engine event streams (jcode ndjson, codex JSONL). Handles watchdog-killed cycles with no done event via a model-hint fallback that must never override an actual completed model; codex-final-text.py converts JSONL to clean summary text without leaking reasoning.

## Related

- part of [[auto-loop-core-engine]]
- produces [[budget-spend-accounting]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
