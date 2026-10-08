---
name: Registry history archival
slug: registry-history-archival
type: system
sources:
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
sources_digest: e1f03a784f0cc33f0cfca177e13c34aa09a5af68f354504d4c93c2597bc2f823
links:
  - to: operational-guard-tripwires
    relation: uses
    description: >-
      Shares the fail-closed, atomic-write, SHA-verified design philosophy with
      the other ops guards.
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

registry-archive.py deterministically archives stale history from memories/candidate-registry.md into monthly files, moving maintenance notes older than --note-age-days and frozen PART A/Cycle N sections older than --section-age-days, replacing each batch with a pointer line. Enforces strict invariants: the protected live region must remain byte-identical, anchor headings unique, and reconstruction verified via SHA-256 before any write. Fail-closed (any violation exits 2, writes nothing), compare-and-swap on mtime to prevent concurrent edits, content-deduplicated appends for crash-safe reruns, and a 5-copy backup rotation. --check deliberately suppresses invariant failures to avoid killing the loop's return moment.

## Related

- uses [[operational-guard-tripwires]] — Shares the fail-closed, atomic-write, SHA-verified design philosophy with the other ops guards.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
