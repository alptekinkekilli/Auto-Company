---
name: State snapshot probe
slug: state-snapshot-probe
type: system
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: b49055f6ad2667278243a5d453a6f3a32f13b362f453588327ababae654d5019
links:
  - to: auto-loop-core-engine
    relation: produces
    description: Its DELTA line feeds the idle-skip decision
  - to: budget-spend-accounting
    relation: uses
    description: 'idle detection consumes the DELTA: none output'
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

A read-only probe that collapses per-cycle state checks into one grep-friendly report of five watched surfaces, computing a DELTA against the previous snapshot so an unchanged world can be dismissed without re-probing. Always exits 0 so a probe failure never kills the calling cycle; errored fields print as ERROR and are excluded from DELTA on both sides.

## Related

- produces [[auto-loop-core-engine]] — Its DELTA line feeds the idle-skip decision
- uses [[budget-spend-accounting]] — idle detection consumes the DELTA: none output
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
