---
name: idle-skip mechanism
slug: idle-skip-mechanism
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 27bc43671255e785f102cc1ce1986edb26bf935290cbb8797272760b4c648fe7
links:
  - to: auto-loop-core-engine
    relation: part_of
generator:
  version: 1
covers:
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
---
<!-- context:generated:start -->
## Summary

Idle detection keys off the snapshot text `DELTA: none` and fails open (unavailable snapshot treated as not idle). The skip branch never calls a model, always runs the OPREQ ledger step before sleeping, and writes last-full-cycle.date only on success; the first cycle of a UTC day is never skipped and the kill switch is read at call time.

## Related

- part of [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
