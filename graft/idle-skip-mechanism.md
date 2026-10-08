---
name: idle-skip mechanism
slug: idle-skip-mechanism
type: concept
sources:
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 876da2627d2b04ac153602cb08a700c6c453d5779c9b43bc922fc9550a3b9fd6
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: _idle_skip_due and the skip branch live in auto-loop.sh
  - to: operator-request-notification
    relation: uses
    description: The skip branch runs operator_request_notify.py before sleeping
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The idle-skip branch never calls a model, always runs the operator_request_notify.py OPREQ ledger step before sleeping, and writes last-full-cycle.date only on success. The first cycle of a UTC day is never skipped; the kill switch IDLE_SKIP_ENABLED is read at call time; the consensus note maintains one line per day with a running count and first-skip start time. Idle detection is based on the snapshot text 'DELTA: none' and fails open (unavailable snapshot = not idle).

## Related

- part of [[auto-loop-core-engine]] — _idle_skip_due and the skip branch live in auto-loop.sh
- uses [[operator-request-notification]] — The skip branch runs operator_request_notify.py before sleeping
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
