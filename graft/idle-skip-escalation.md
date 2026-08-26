---
name: Idle-skip & escalation
slug: idle-skip-escalation
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 02e6bade9475fcf448e6804a75686e5e829208187336182b8ed44472ba534518
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Idle-skip and escalation are functions of auto-loop.sh.
  - to: state-snapshot-probe
    relation: uses
    description: 'Idle detection reads the snapshot''s DELTA: none line.'
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

The idle-skip mechanism (first cycle of a UTC day never skipped, kill switch read at call time, consensus note one line per day) and the one-shot operator escalation (consumed exactly once; a refusal leaves it ARMED rather than burning an approval). Both live in auto-loop.sh and are driven by runtime.env flags.

## Related

- part of [[auto-loop-core-engine]] — Idle-skip and escalation are functions of auto-loop.sh.
- uses [[state-snapshot-probe]] — Idle detection reads the snapshot's DELTA: none line.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
