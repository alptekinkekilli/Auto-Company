---
name: Registry archiver
slug: registry-archiver
type: system
sources:
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
sources_digest: e1f03a784f0cc33f0cfca177e13c34aa09a5af68f354504d4c93c2597bc2f823
links:
  - to: auto-company-loop-core
    relation: uses
    description: Runs before analysts read the registry to keep the live file small.
generator:
  version: 1
covers:
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

Deterministically archives stale history from memories/candidate-registry.md into monthly files, shrinking the live file analysts read daily. Enforces strict invariants: the protected live region must remain byte-identical, anchor headings unique, and reconstruction verified via SHA-256 before any write. Fail-closed (any invariant violation exits 2 and writes nothing), with a compare-and-swap on the live file's mtime to prevent concurrent edits.

## Related

- uses [[auto-company-loop-core]] — Runs before analysts read the registry to keep the live file small.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
