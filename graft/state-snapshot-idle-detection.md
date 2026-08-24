---
name: State snapshot & idle detection
slug: state-snapshot-idle-detection
type: system
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: 4cd8f958c15e5cb5afda42aee615989ace41e86301c47174bf2e30439e222b0b
links:
  - to: auto-loop-core-engine
    relation: uses
    description: 'idle detection based on DELTA: none snapshot text'
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

Produces a local-only state snapshot with DELTA change detection (errored fields excluded from next DELTA), and drives idle-skip: first cycle of a UTC day never skipped, kill switch read at call time, consensus note one line per day.

## Related

- uses [[auto-loop-core-engine]] — idle detection based on DELTA: none snapshot text
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
