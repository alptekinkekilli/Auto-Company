---
name: Idle-skip audit trail
slug: idle-skip-audit-trail
type: file
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
sources_digest: fbdec8360c46d903ea73260434f53bcab29a4624612d37a127ac69496f0acc48
links: []
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

Records model-free idle-skip events into consensus.md as a single markdown line per UTC day so the IDLE-SKIP path leaves an auditable 'checked, nothing moved' trace without bloating the prompt. Atomic write via tempfile+os.replace; the ndjson trail is only mentioned in output text, not written by this script, and parsing assumes the exact line format produced by build_line.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
