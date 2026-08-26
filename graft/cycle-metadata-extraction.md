---
name: Cycle metadata extraction
slug: cycle-metadata-extraction
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 541464bd69d50fdca3952e3222a99b6b158e3cc607e0496f0851a76e50915f1d
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: extract_cycle_metadata is a function of auto-loop.sh.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
---
<!-- context:generated:start -->
## Summary

extract_cycle_metadata() in auto-loop.sh plus the companion codex-final-text.py convert raw engine output (Codex plain-prose or Claude JSON) into structured CYCLE_TYPE/CYCLE_SUBTYPE/RESULT_TEXT without leaking reasoning or thread metadata. Must never kill the loop when Codex is routed through alternation or fallback (APP-240).

## Related

- part of [[auto-loop-core-engine]] — extract_cycle_metadata is a function of auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
