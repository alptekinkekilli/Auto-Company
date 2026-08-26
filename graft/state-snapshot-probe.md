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
    description: >-
      The snapshot DELTA line drives idle-skip and discretionary budget
      decisions in auto-loop.sh.
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

state-snapshot.py collapses per-cycle state checks into one grep-friendly report of five watched surfaces, computing a DELTA against the previous snapshot so an unchanged world can be dismissed without re-probing. Read-only toward the world, always exits 0.

## Related

- produces [[auto-loop-core-engine]] — The snapshot DELTA line drives idle-skip and discretionary budget decisions in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
