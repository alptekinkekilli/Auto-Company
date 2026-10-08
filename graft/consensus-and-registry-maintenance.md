---
name: Consensus and registry maintenance
slug: consensus-and-registry-maintenance
type: system
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 47d5d806a8f48f41817b9bce5cc8e759d9ed04b244627e858664aeef6c9cf42b
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
sources_digest: efa58169bc427a9a576fdde72860fc0ba14236e176c283ca33a497042d3b3804
links:
  - to: ledger-integrity-guard
    relation: uses
    description: >-
      ledger-guard.py runs before consensus-prune and exempts the prune
      transition via crafted archive notes and post_metrics; _rebase_after_prune
      reconciles baselines after legitimate pruning.
generator:
  version: 1
covers:
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L61-L66'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L69-L70'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L73-L74'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L77-L81'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L84-L91'
  - symbol: _section_sizes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L94-L99'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L102-L103'
  - symbol: _split_section
    kind: function
    at: 'scripts/ops/consensus-prune.py:L106-L120'
  - symbol: _parse_entries
    kind: function
    at: 'scripts/ops/consensus-prune.py:L123-L153'
  - symbol: _check_monotonic
    kind: function
    at: 'scripts/ops/consensus-prune.py:L156-L163'
  - symbol: _archive_path
    kind: function
    at: 'scripts/ops/consensus-prune.py:L166-L167'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L170-L327'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L190-L208'
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

Two archival harnesses that keep the live memory files small enough to avoid the [PROMPT-SIZE] brake: consensus-prune.py archives old 'What We Did This Cycle' entries byte-exact to monthly files with a sha256-stamped header, requiring monotonic cycle numbers and rejecting unknown bullets; registry-archive.py moves stale maintenance notes and frozen PART A/Cycle N sections to monthly files, keeping the protected live region byte-identical and verifying reconstruction via SHA-256 before any write. Both are fail-closed, atomic, and coordinate with ledger-guard.py's baselines.

## Related

- uses [[ledger-integrity-guard]] — ledger-guard.py runs before consensus-prune and exempts the prune transition via crafted archive notes and post_metrics; _rebase_after_prune reconciles baselines after legitimate pruning.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
