---
name: Cycle counter & metadata
slug: cycle-counter-metadata
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 16f57a317e5f38443d3956fb9ab4976945ef01692772d4b9938de7e7b8b4e5e9
links:
  - to: auto-loop-core
    relation: part_of
    description: Seed block and extract_cycle_metadata() live in auto-loop.sh.
  - to: budget-spend-accounting
    relation: uses
    description: >-
      Per-cycle harness/provider metadata (CYCLE_HARNESS_USED,
      CYCLE_PROVIDER_USED) override global LOOP_HARNESS for cost attribution.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The monotonic cycle-counter seeding and per-cycle metadata extraction in auto-loop.sh. The counter must be monotonic across redeploys (persisted file wins, self-heals to highest on-disk cycle-NNNN, digits-only strip on corrupt values) and must run before engine selection and loop_count increment so off-hours ticks don't burn cycle numbers. Metadata extraction must never kill the loop when Codex is routed through alternation/fallback.

## Related

- part of [[auto-loop-core]] — Seed block and extract_cycle_metadata() live in auto-loop.sh.
- uses [[budget-spend-accounting]] — Per-cycle harness/provider metadata (CYCLE_HARNESS_USED, CYCLE_PROVIDER_USED) override global LOOP_HARNESS for cost attribution.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
