---
name: Idle-skip & escalation
slug: idle-skip-escalation
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 215b69606a8c58c65539e98063fb19dfae6025e516b16c4f6a53302e634a1bfe
links:
  - to: auto-loop-core
    relation: part_of
    description: >-
      _idle_skip_due, apply_cycle_escalation, _consume_escalation,
      _directive_is_pending live in auto-loop.sh.
  - to: ops-probe-audit-scripts
    relation: uses
    description: 'Idle detection consumes state-snapshot''s DELTA: none output.'
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Two one-shot control mechanisms in auto-loop.sh: idle-skip (first cycle of a UTC day never skipped, kill switch read at call time, consensus note one line/day, skip branch never calls a model and always runs the OPREQ ledger step) and one-shot operator escalation (consumed exactly once; a refusal leaves it ARMED rather than burning an approval).

## Related

- part of [[auto-loop-core]] — _idle_skip_due, apply_cycle_escalation, _consume_escalation, _directive_is_pending live in auto-loop.sh.
- uses [[ops-probe-audit-scripts]] — Idle detection consumes state-snapshot's DELTA: none output.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
