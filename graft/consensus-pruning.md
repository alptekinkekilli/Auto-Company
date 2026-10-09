---
name: Consensus Pruning
slug: consensus-pruning
type: system
sources:
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 82fd9dfa80c4f0c916c506e6a44db71dbfd6ee1c0421bcedf8d255b77c3bfd7e
  - path: tests/test_consensus_prune.py
    hash: 35e0bdc2dd8148ac41d2e6463ee61fdb69732ee19e5835114387210b8558e37e
sources_digest: be3d0ebea0c02c24fa9f967be4388553cf873074178673f7c304f7b7f6bc0912
links:
  - to: auto-loop-harness
    relation: part_of
    description: >-
      Invoked after ledger-guard.py in auto-loop.sh, gated on empty
      cycle_failed_reason
generator:
  version: 1
covers:
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

consensus-prune.py prunes old entries from the team consensus markdown file, archiving them byte-exactly to docs/operations/consensus-archive-*.md and keeping the newest N entries (default 12). Skips on unknown bullets, non-monotonic cycle numbers, missing sections, invalid UTF-8, or unwritable archive dir; escalates an alarm after three consecutive skips; dedups archive blocks via SHA-256. Integrates with ledger-guard.py by ensuring archive notes don't match its INCIDENT_RE regex.

## Related

- part of [[auto-loop-harness]] — Invoked after ledger-guard.py in auto-loop.sh, gated on empty cycle_failed_reason
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
