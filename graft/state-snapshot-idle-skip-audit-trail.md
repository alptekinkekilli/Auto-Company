---
name: State snapshot & idle-skip audit trail
slug: state-snapshot-idle-skip-audit-trail
type: system
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: 969b98e16ebbe3d3801d138dc83ce3416bc6952d1607957662c7a2f13a1e0234
links:
  - to: loop-lifecycle-monitoring
    relation: uses
    description: >-
      Both read/write consensus.md and logs under the app root that the loop
      maintains.
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

One-call probes that collapse per-cycle state checks into a single turn. state-snapshot.py hashes five watched surfaces and computes a DELTA against the previous snapshot, always exiting 0 so a probe failure never kills the cycle. idle-skip-note.py records model-free idle-skip events into consensus.md as one line per UTC day, leaving an auditable 'checked, nothing moved' trace without bloating the prompt.

## Related

- uses [[loop-lifecycle-monitoring]] — Both read/write consensus.md and logs under the app root that the loop maintains.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
