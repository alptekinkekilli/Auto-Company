---
name: registry archive & state snapshot
slug: registry-archive-state-snapshot
type: system
sources:
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: a88e66891d72edacdcb93ca4238e91fd45f65b2e9388bab99cdee5258314c168
links:
  - to: operator-escalation-gate
    relation: uses
    description: >-
      state-snapshot's DELTA on the auditor report hash implements
      OPREQ-INFRA-ANALYST-ROUTING-001 Option B.
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

Deterministic maintenance of the candidate-registry and a one-call state probe. registry-archive.py moves stale history into monthly files with strict invariants (protected live region byte-identical, unique anchors, SHA-256 verification before write, compare-and-swap on mtime, backup rotation), failing closed on any violation. state-snapshot.py collapses the per-cycle fan-out of state checks into one turn, computing a DELTA against the last snapshot so an unchanged world is dismissed without re-probing; 'none' never means 'nothing to do'.

## Related

- uses [[operator-escalation-gate]] — state-snapshot's DELTA on the auditor report hash implements OPREQ-INFRA-ANALYST-ROUTING-001 Option B.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
