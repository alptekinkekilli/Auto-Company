---
name: State snapshot
slug: state-snapshot
type: system
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: b22d6b1127d5b052b726fc0dc5a244376cf2f7f1b8d621a83596632c9199dcd2
links:
  - to: auto-loop-core-engine
    relation: produces
  - to: work-window-brake
    relation: produces
    description: The DELTA line is the input the work-window brake parses.
generator:
  version: 1
covers:
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

A one-call probe that collapses the per-cycle fan-out of state checks into a single turn, hashing five watched surfaces (directives, OPREQ ledger, Wowcar sources) and computing a DELTA against the previous snapshot. Always exits 0 so a probe failure never kills the cycle; 'none' does not mean 'nothing to do' — standing orders still apply. Implements OPREQ-INFRA-ANALYST-ROUTING-001 Option B by making the auditor report hash delta-visible.

## Related

- produces [[auto-loop-core-engine]]
- produces [[work-window-brake]] — The DELTA line is the input the work-window brake parses.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
