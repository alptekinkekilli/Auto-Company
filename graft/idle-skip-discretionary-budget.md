---
name: Idle-skip & discretionary budget
slug: idle-skip-discretionary-budget
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 64277de0e72b8cff6f26eb7ff8bf171f4f0416981de7c34a0998e158ee344335
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Idle-skip and discretionary-cap logic live in auto-loop.sh.
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

Two spending-control mechanisms in auto-loop.sh: idle detection based on snapshot text `DELTA: none` (fails open, first cycle of a UTC day never skipped, kill switch read at call time), and a discretionary daily cap that injects a warning line into the prompt once the day's spend reaches a threshold. The consensus note maintains one line per day with a running count.

## Related

- part of [[auto-loop-core-engine]] — Idle-skip and discretionary-cap logic live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
