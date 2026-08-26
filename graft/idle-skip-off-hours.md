---
name: idle-skip & off-hours
slug: idle-skip-off-hours
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: d324d5c33b5fcfe86ac145b8400d179c4821b72ca820cf6350f6e790858e2a18
links:
  - to: auto-loop-core-loop
    relation: part_of
    description: '_idle_skip_due, _window_active, and the skip branch live in auto-loop.sh.'
  - to: escalation-operator-requests
    relation: uses
    description: The skip branch runs operator_request_notify.py before sleeping.
generator:
  version: 1
covers:
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
  - symbol: file_sha16
    kind: function
    at: 'scripts/ops/state-snapshot.py:L54-L61'
  - symbol: directive_state
    kind: function
    at: 'scripts/ops/state-snapshot.py:L64-L72'
  - symbol: opreq_open
    kind: function
    at: 'scripts/ops/state-snapshot.py:L75-L87'
  - symbol: wowcar_sources
    kind: function
    at: 'scripts/ops/state-snapshot.py:L90-L104'
  - symbol: main
    kind: function
    at: 'scripts/ops/state-snapshot.py:L107-L166'
---
<!-- context:generated:start -->
## Summary

Idle detection (DELTA: none snapshot text) and the idle-skip mechanism: the first cycle of a UTC day is never skipped, the kill switch is read at call time, the skip branch never calls a model, always runs the OPREQ ledger step before sleeping, and writes last-full-cycle.date only on success. Off-hours polling defaults to 900s and logs the transition once. The business-hours gate (_window_active) fails open on malformed config so a typo never parks the company.

## Related

- part of [[auto-loop-core-loop]] — _idle_skip_due, _window_active, and the skip branch live in auto-loop.sh.
- uses [[escalation-operator-requests]] — The skip branch runs operator_request_notify.py before sleeping.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
