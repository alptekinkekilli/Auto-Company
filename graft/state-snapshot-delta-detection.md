---
name: State snapshot & delta detection
slug: state-snapshot-delta-detection
type: system
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: b49055f6ad2667278243a5d453a6f3a32f13b362f453588327ababae654d5019
links:
  - to: cycle-orchestration-engine-routing
    relation: produces
    description: >-
      The idle-skip mechanism reads the snapshot's DELTA: none line to decide
      whether to skip.
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

state-snapshot.py collapses per-cycle state checks into one probe, hashing five watched surfaces and computing a DELTA against the previous snapshot. Advisory and read-only toward the world (only writes its own state file), always exits 0 so a probe failure never kills the cycle, and 'none' does not mean 'nothing to do'.

## Related

- produces [[cycle-orchestration-engine-routing]] — The idle-skip mechanism reads the snapshot's DELTA: none line to decide whether to skip.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
