---
name: Registry Archive & State
slug: registry-archive-state
type: system
sources:
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: 5135d0b64fd2e4f66025adb9287ccb0b11d04d3161c56237fb20df4febba5bf0
links:
  - to: operator-escalation-gate
    relation: uses
    description: >-
      state-snapshot.py makes the auditor report hash delta-visible per
      OPREQ-INFRA-ANALYST-ROUTING-001.
generator:
  version: 1
covers:
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
  - symbol: die
    kind: function
    at: 'scripts/ops/registry-archive.py:L55-L57'
  - symbol: sha
    kind: function
    at: 'scripts/ops/registry-archive.py:L60-L61'
  - symbol: heading_line_starts
    kind: function
    at: 'scripts/ops/registry-archive.py:L64-L65'
  - symbol: protected_span
    kind: function
    at: 'scripts/ops/registry-archive.py:L68-L80'
  - symbol: plan_note_chunks
    kind: function
    at: 'scripts/ops/registry-archive.py:L83-L105'
  - symbol: plan_section_chunks
    kind: function
    at: 'scripts/ops/registry-archive.py:L108-L140'
  - symbol: interleave
    kind: function
    at: 'scripts/ops/registry-archive.py:L143-L149'
  - symbol: main
    kind: function
    at: 'scripts/ops/registry-archive.py:L152-L340'
  - symbol: month_of
    kind: function
    at: 'scripts/ops/registry-archive.py:L250-L251'
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

Deterministic maintenance of the candidate-registry and consensus state. registry-archive.py moves stale history into monthly files with strict invariants (protected live region byte-identical, SHA-256 verified reconstruction, compare-and-swap on mtime, fail-closed). idle-skip-note.py records model-free idle-skip events as one line per UTC day in consensus.md with atomic write. state-snapshot.py collapses per-cycle state checks into one turn with a DELTA line.

## Related

- uses [[operator-escalation-gate]] — state-snapshot.py makes the auditor report hash delta-visible per OPREQ-INFRA-ANALYST-ROUTING-001.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
