---
name: cycle metadata extraction
slug: cycle-metadata-extraction
type: concept
sources:
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: a2275503526f7c6027a9cae8b0ff17f8e3b22d00e8ccca9ebccabc3e4f7429a8
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: >-
      extract_cycle_metadata() and run_engine_cycle() live in auto-loop.sh and
      are tested by extracting them via awk
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

extract_cycle_metadata() parses engine output to produce CYCLE_TYPE, CYCLE_SUBTYPE, RESULT_TEXT and per-cycle harness/provider attribution. A regression (APP-240) fixed a bug where the loop was killed when Codex was routed through alternation/fallback; the fix must never kill the loop or container. Per-cycle CYCLE_HARNESS_USED/CYCLE_PROVIDER_USED override any global LOOP_HARNESS value.

## Related

- part of [[auto-loop-core-engine]] — extract_cycle_metadata() and run_engine_cycle() live in auto-loop.sh and are tested by extracting them via awk
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
