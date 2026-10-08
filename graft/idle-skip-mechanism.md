---
name: idle-skip mechanism
slug: idle-skip-mechanism
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 40304af6c59508b4e0895cdf65755d8a8a5be97b1ef10bbc7cd64060876c3fe3
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: _idle_skip_due and the skip branch live in auto-loop.sh.
  - to: operator-request-notify
    relation: uses
    description: The skip branch always runs operator_request_notify.py before sleeping.
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

Idle detection keys off the snapshot text `DELTA: none`; when idle, the loop skips the model call entirely, always runs the operator_request_notify OPREQ ledger step before sleeping, and writes last-full-cycle.date only on success. The first cycle of a UTC day is never skipped, the kill switch is read at call time, and the idle check fails open (unavailable snapshot = not idle).

## Related

- part of [[auto-loop-core-engine]] — _idle_skip_due and the skip branch live in auto-loop.sh.
- uses [[operator-request-notify]] — The skip branch always runs operator_request_notify.py before sleeping.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
