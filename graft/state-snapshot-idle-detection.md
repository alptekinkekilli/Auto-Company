---
name: State snapshot & idle detection
slug: state-snapshot-idle-detection
type: system
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: 969b98e16ebbe3d3801d138dc83ce3416bc6952d1607957662c7a2f13a1e0234
links:
  - to: auto-loop-core-auto-loop-sh
    relation: produces
    description: >-
      Snapshot DELTA and idle-skip note drive the idle-skip branch and
      discretionary budget idle check.
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

state-snapshot.py collapses per-cycle state checks into one grep-friendly report with a DELTA line against the previous snapshot, always exiting 0 so probe failure never kills the cycle. Feeds idle detection: DELTA:none means world unchanged. Advisory and read-only toward the world except its own state file.

## Related

- produces [[auto-loop-core-auto-loop-sh]] — Snapshot DELTA and idle-skip note drive the idle-skip branch and discretionary budget idle check.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
