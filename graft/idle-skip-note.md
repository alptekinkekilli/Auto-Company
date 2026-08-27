---
name: Idle-skip note
slug: idle-skip-note
type: system
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
sources_digest: fbdec8360c46d903ea73260434f53bcab29a4624612d37a127ac69496f0acc48
links:
  - to: auto-company-loop-core
    relation: uses
    description: Called on the IDLE-SKIP path to leave an auditable trace.
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

Records model-free idle-skip events into consensus.md as a single markdown line per UTC day, so the auto-loop's IDLE-SKIP path leaves an auditable 'checked, nothing moved' trace without bloating the prompt. Atomic write via temp file + os.replace; any read/write error exits non-zero without touching the original, which the calling loop treats as best-effort.

## Related

- uses [[auto-company-loop-core]] — Called on the IDLE-SKIP path to leave an auditable trace.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
