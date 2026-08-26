---
name: Idle-skip & escalation one-shot semantics
slug: idle-skip-escalation-one-shot-semantics
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: bde710ae0f019d2a4747ee42b75e086bfccfaa40243ca83cfd0812eb490946b9
links:
  - to: auto-loop-core-engine
    relation: implements
    description: The _idle_skip_due and apply_cycle_escalation functions
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

Two cross-cutting invariants in the loop: idle-skip never calls a model, always runs the OPREQ ledger step before sleeping, and the first cycle of a UTC day is never skipped; escalation is consumed exactly once and a refusal leaves it ARMED rather than burning an approval. Both read their kill-switch/armed flags from runtime.env at call time.

## Related

- implements [[auto-loop-core-engine]] — The _idle_skip_due and apply_cycle_escalation functions
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
