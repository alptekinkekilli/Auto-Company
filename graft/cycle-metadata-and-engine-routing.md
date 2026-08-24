---
name: Cycle metadata and engine routing
slug: cycle-metadata-and-engine-routing
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: tests/test_cycle_metadata.sh
    hash: 66a21f12ac379be58cda6db2e98c410b11104c0fc2c2d8c6efdffd422dcd3988
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: b71af85a8e3d37ddedc24ebaad80325f373a40d492b8573185b04ec3236f0e13
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Functions extracted from auto-loop.sh.
  - to: budget-and-spend-accounting
    relation: uses
    description: >-
      REVISE-2 gate A5 persists a claude attempt's cost under its own run ID
      before a codex retry.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

extract_cycle_metadata() and run_engine_cycle() attribute each cycle's harness/provider/type and route between claude→jcode and codex→cli engines in the mixed harness. Per-cycle variables override any global LOOP_HARNESS; unmeasured or zero-cost jcode cycles fail and latch; unparseable attempt costs block retries.

## Related

- part of [[auto-loop-core-engine]] — Functions extracted from auto-loop.sh.
- uses [[budget-and-spend-accounting]] — REVISE-2 gate A5 persists a claude attempt's cost under its own run ID before a codex retry.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
