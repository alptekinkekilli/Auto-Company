---
name: Idle-skip and escalation
slug: idle-skip-and-escalation
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 8047ae1ceb7eac76beba89e0584912e2500baee4f68bb2f372c872739a2c7193
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
sources_digest: 46caad3ceb4d42f4b07e07f0064997e434ed75150f22161237212158248a860a
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Both mechanisms are functions extracted from auto-loop.sh.
generator:
  version: 1
covers:
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
---
<!-- context:generated:start -->
## Summary

Two one-shot mechanisms in auto-loop.sh: idle-skip (first cycle of a UTC day never skipped, kill switch read at call time, consensus note one line per day) and operator escalation (consumed exactly once, refusal leaves it ARMED).

## Related

- part of [[auto-loop-core-engine]] — Both mechanisms are functions extracted from auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
