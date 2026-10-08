---
name: Registry Archive & Consensus Pruning
slug: registry-archive-consensus-pruning
type: system
sources:
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 82fd9dfa80c4f0c916c506e6a44db71dbfd6ee1c0421bcedf8d255b77c3bfd7e
  - path: tests/test_consensus_prune.py
    hash: 35e0bdc2dd8148ac41d2e6463ee61fdb69732ee19e5835114387210b8558e37e
sources_digest: d40d8d20791bd40636b5196beeaabaf7951a40a3bef64984c2c32d0f5696e4ab
links:
  - to: auto-company-ops-scripts
    relation: part_of
    description: >-
      registry-archive.py is one of the ops scripts; consensus-prune is wired
      into auto-loop.sh after ledger-guard.
  - to: auto-loop-harness
    relation: configures
    description: >-
      consensus-prune.py is invoked from auto-loop.sh, gated on an empty
      cycle_failed_reason.
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
  - symbol: check
    kind: function
    at: 'tests/test_consensus_prune.py:L17-L20'
  - symbol: newapp
    kind: function
    at: 'tests/test_consensus_prune.py:L23-L26'
  - symbol: consensus
    kind: function
    at: 'tests/test_consensus_prune.py:L29-L30'
  - symbol: entry
    kind: function
    at: 'tests/test_consensus_prune.py:L33-L38'
  - symbol: doc
    kind: function
    at: 'tests/test_consensus_prune.py:L41-L51'
  - symbol: run
    kind: function
    at: 'tests/test_consensus_prune.py:L54-L62'
  - symbol: guard
    kind: function
    at: 'tests/test_consensus_prune.py:L65-L68'
---
<!-- context:generated:start -->
## Summary

Deterministic archival of stale history to keep live files small: registry-archive.py moves old maintenance notes and frozen PART A/Cycle sections from memories/candidate-registry.md into monthly archive files (byte-identical protected region, SHA-256 verified before write, compare-and-swap on mtime, backup rotation), and consensus-prune.py prunes old entries from consensus.md into docs/operations/consensus-archive-*.md with SHA-256 dedup. Both are fail-closed and verified by integration tests.

## Related

- part of [[auto-company-ops-scripts]] — registry-archive.py is one of the ops scripts; consensus-prune is wired into auto-loop.sh after ledger-guard.
- configures [[auto-loop-harness]] — consensus-prune.py is invoked from auto-loop.sh, gated on an empty cycle_failed_reason.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
