---
name: idle-skip audit trail
slug: idle-skip-audit-trail
type: file
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
sources_digest: fbdec8360c46d903ea73260434f53bcab29a4624612d37a127ac69496f0acc48
links:
  - to: loop-lifecycle-monitoring
    relation: uses
    description: Called by the auto-loop's IDLE-SKIP path to record skipped cycles.
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

Records model-free idle-skip events into consensus.md as one line per UTC day, leaving an auditable 'checked, nothing moved' trace without bloating the prompt. Atomic write, best-effort from the loop's perspective.

## Related

- uses [[loop-lifecycle-monitoring]] — Called by the auto-loop's IDLE-SKIP path to record skipped cycles.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
