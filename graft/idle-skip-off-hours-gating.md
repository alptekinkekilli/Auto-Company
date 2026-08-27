---
name: Idle-skip & off-hours gating
slug: idle-skip-off-hours-gating
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 5ce5879c900019e45bbfb02c125cffa051e49fb2a51cfc89d878c0d76136263a
links:
  - to: auto-loop-core-engine
    relation: implements
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

The loop skips idle cycles (DELTA: none) and off-hours ticks without burning cycle numbers or external calls; the first cycle of a UTC day is never skipped, the kill switch is read at call time, and off-hours transition is logged once. The business-hours gate fails open on malformed config so a typo never parks the company.

## Related

- implements [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
