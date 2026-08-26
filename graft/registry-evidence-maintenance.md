---
name: Registry & Evidence Maintenance
slug: registry-evidence-maintenance
type: system
sources:
  - path: scripts/ops/extract-axis-evidence.py
    hash: 3f3d55a2a285cd52ab3b0d286b1f908b877283bfde69b03e442d10758080f567
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
sources_digest: c76c1bfa2bbea1348a9194f499ff4138d2d6ca30ea722e83408cdaedd4335a51
links:
  - to: outreach-eligibility-evidence
    relation: uses
    description: >-
      g4-check.py and send-gate.py read the registry that registry-archive.py
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
---
<!-- context:generated:start -->
## Summary

Maintains and extracts evidence from the candidate registry and research docs. registry-archive.py moves stale history into monthly files with strict invariants (protected live region byte-identical, SHA-256 verification, compare-and-swap on mtime, fail-closed on any violation). extract-axis-evidence.py extracts screened axis headings/bodies from discovery-scan markdown, failing closed on any unreadable file or count mismatch. idle-skip-note.py records model-free idle-skip events as one line per UTC day in consensus.md with atomic replace.

## Related

- uses [[outreach-eligibility-evidence]] — g4-check.py and send-gate.py read the registry that registry-archive.py maintains.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
