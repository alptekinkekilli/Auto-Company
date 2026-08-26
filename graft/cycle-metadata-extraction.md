---
name: Cycle metadata extraction
slug: cycle-metadata-extraction
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 5c87bb000e976620696f6f8e0a8a8caf8706bec9246b6875d49b41e875be3744
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: extract_cycle_metadata() is a function in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Parses engine output into per-cycle metadata (CYCLE_TYPE, CYCLE_SUBTYPE, RESULT_TEXT) and converts Codex JSONL event streams into clean summary text via codex-final-text.py, ensuring reasoning and thread metadata are not leaked. Must never kill the loop when Codex is routed through alternation or fallback (APP-240).

## Related

- part of [[auto-loop-core-engine]] — extract_cycle_metadata() is a function in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
