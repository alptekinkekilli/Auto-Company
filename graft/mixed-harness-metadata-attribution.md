---
name: mixed harness metadata attribution
slug: mixed-harness-metadata-attribution
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 0f9d2306b9064e090882ef01e8aa4c854390412ce3feade5f6f8c7b3c4757107
links:
  - to: auto-loop-sh-core-loop
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Per-cycle metadata (CYCLE_HARNESS_USED, CYCLE_PROVIDER_USED) must override global LOOP_HARNESS; stale jcode cost must not leak into subsequent CLI cycles; unmeasured/zero-cost jcode cycles fail and latch; unparseable attempt costs block retry.

## Related

- part of [[auto-loop-sh-core-loop]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
