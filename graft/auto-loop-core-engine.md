---
name: Auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 8047ae1ceb7eac76beba89e0584912e2500baee4f68bb2f372c872739a2c7193
sources_digest: 09490ff62dd4b45d3340d0b71341695ef1b4205f1305a986d18cf8036c7ab394
links:
  - to: prod-mechanism-guard
    relation: validates
    description: >-
      test_prod_mechanism_guard.sh and prod-mechanism-guard.py block edits to
      auto-loop.sh unless an approval marker exists.
  - to: state-snapshot-probe
    relation: uses
    description: >-
      auto-loop.sh reads the snapshot DELTA line to decide idle-skip and
      discretionary budget.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop that runs cycles, selects engines (claude→jcode, codex→cli), enforces budget gates, idle-skip, escalation, and prompt assembly. It is the protected production surface guarded by prod-mechanism-guard.py and the subject of most regression tests.

## Related

- validates [[prod-mechanism-guard]] — test_prod_mechanism_guard.sh and prod-mechanism-guard.py block edits to auto-loop.sh unless an approval marker exists.
- uses [[state-snapshot-probe]] — auto-loop.sh reads the snapshot DELTA line to decide idle-skip and discretionary budget.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
