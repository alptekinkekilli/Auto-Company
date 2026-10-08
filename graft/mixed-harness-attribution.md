---
name: mixed-harness attribution
slug: mixed-harness-attribution
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: a6f74885e019dce4ee1f3a8a0a8c876891463e88332a6f1e136eb7a2a6f2ea74
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: >-
      run_engine_cycle() and extract_cycle_metadata() implement this in
      auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

When claude→jcode and codex→cli run in the same loop, per-cycle variables CYCLE_HARNESS_USED and CYCLE_PROVIDER_USED override any global LOOP_HARNESS. Stale jcode cost must not leak into subsequent CLI cycles; unmeasured or zero-cost jcode cycles fail and latch; unparseable attempt costs block the retry; and the REVISE-2 gate A5 persists a claude attempt's cost under its own run ID before a codex retry.

## Related

- part of [[auto-loop-core-engine]] — run_engine_cycle() and extract_cycle_metadata() implement this in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
