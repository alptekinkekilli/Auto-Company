---
name: Consensus & registry maintenance
slug: consensus-registry-maintenance
type: system
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 721ea1c0b942cae4679c4472f4ec5547e4655cd9e94c12c9ddc8fccd2f922821
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
sources_digest: 5da307c5bc35889c615515b64228d24e1e657711e23677ca1e156f05bc1f0c6b
links: []
generator:
  version: 1
covers:
  - symbol: _load_runtime_env
    kind: function
    at: 'scripts/ops/consensus-prune.py:L69-L80'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L83-L88'
  - symbol: _env_flag
    kind: function
    at: 'scripts/ops/consensus-prune.py:L91-L92'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L95-L96'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L99-L100'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L103-L107'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L110-L117'
  - symbol: _section_sizes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L120-L125'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L128-L129'
  - symbol: _split_section
    kind: function
    at: 'scripts/ops/consensus-prune.py:L132-L146'
  - symbol: _parse_entries
    kind: function
    at: 'scripts/ops/consensus-prune.py:L149-L186'
  - symbol: _check_monotonic
    kind: function
    at: 'scripts/ops/consensus-prune.py:L189-L196'
  - symbol: _archive_path
    kind: function
    at: 'scripts/ops/consensus-prune.py:L199-L200'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L203-L373'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L227-L245'
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

Maintenance scripts that keep long-lived memory files small and auditable. consensus-prune.py archives old 'What We Did This Cycle' entries byte-exact with sha256-stamped headers, deliberately avoiding ledger-guard's INCIDENT_RE words so it doesn't trigger the content-loss alarm, and logs state for ledger-guard to exempt the transition. registry-archive.py moves stale history from candidate-registry.md into monthly files, enforcing strict invariants (protected live region byte-identical, unique anchor headings, SHA-256 reconstruction verification) with compare-and-swap on mtime and content-deduplicated appends for crash-safe reruns. idle-skip-note.py records model-free idle-skip events as one auditable line per UTC day.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
