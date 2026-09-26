---
name: mixed-harness attribution
slug: mixed-harness-attribution
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 62a3c4f6dbcb58f9de9410deea3e6471baef56c19fd63ec4821fb443e84e4b8c
links:
  - to: auto-loop-core-engine
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

When claude→jcode and codex→cli run in the same loop, per-cycle CYCLE_HARNESS_USED/CYCLE_PROVIDER_USED override any global LOOP_HARNESS; stale jcode cost must not leak into subsequent CLI cycles, and the REVISE-2 gate A5 persists a claude attempt's cost under its own run ID before a codex retry. Unmeasured/zero-cost jcode cycles fail and latch.

## Related

- part of [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
