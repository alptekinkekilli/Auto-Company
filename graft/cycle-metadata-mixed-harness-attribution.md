---
name: Cycle metadata & mixed-harness attribution
slug: cycle-metadata-mixed-harness-attribution
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 57791d599053b4135bb0ae2f991b84b4d56eb2e1babe290643cf8e3b732bdaa8
links:
  - to: auto-loop-core-engine
    relation: implements
    description: extract_cycle_metadata and run_engine_cycle
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

The invariant that each cycle's metadata and cost are attributed to the actual engine used (claude→jcode, codex→cli), overriding any global LOOP_HARNESS value, and that extract_cycle_metadata never kills the loop when Codex is routed through alternation or fallback. Stale jcode cost must not leak into subsequent CLI cycles.

## Related

- implements [[auto-loop-core-engine]] — extract_cycle_metadata and run_engine_cycle
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
