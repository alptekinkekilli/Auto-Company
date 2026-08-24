---
name: Idle-skip and discretionary budget
slug: idle-skip-and-discretionary-budget
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 28e01b515b90da9a9ce5a0564e5e7c59099e69e61dde0b7002a6c1b86e22e156
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: _idle_skip_due and the discretionary cap wiring live in auto-loop.sh.
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

Idle detection (DELTA: none snapshot text) and the discretionary daily cap that injects a warning line into the prompt. The first cycle of a UTC day is never skipped; the kill switch is read at call time; the skip branch never calls a model and always runs the OPREQ ledger step before sleeping. Idle check fails open (unavailable snapshot = not idle).

## Related

- part of [[auto-loop-core-engine]] — _idle_skip_due and the discretionary cap wiring live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
