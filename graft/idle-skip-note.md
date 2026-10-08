---
name: Idle-skip note
slug: idle-skip-note
type: system
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
sources_digest: fbdec8360c46d903ea73260434f53bcab29a4624612d37a127ac69496f0acc48
links:
  - to: consensus-pruning-ledger-guard
    relation: part_of
    description: Writes into the same consensus.md file the prune/guard protect.
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

Records model-free idle-skip events into consensus.md as one markdown line per UTC day so the IDLE-SKIP path leaves an auditable 'checked, nothing moved' trace without bloating the prompt. Locates the day's line via an HTML comment marker, increments the cycle count, and rewrites atomically; the ndjson trail is only mentioned in output, not written here, and parsing assumes the exact build_line format with conservative fallbacks if it drifts.

## Related

- part of [[consensus-pruning-ledger-guard]] — Writes into the same consensus.md file the prune/guard protect.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
