---
name: Consensus & Memory Maintenance
slug: consensus-memory-maintenance
type: system
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 1a741019d9b78a90dc9121e012850f5bcebd88fbd8527a8b17a4357068ca4684
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/ledger-guard.py
    hash: 5b3098424eada1d1f669995baf5e1dd76ea4fb724c0c524ddc9986ce361128d7
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
sources_digest: 9cda4b6ca67c0e8b481c6eb7cc3fad234eca4b6ed50aad29cbb56029e0e43639
links: []
generator:
  version: 1
covers:
  - symbol: _load_runtime_env
    kind: function
    at: 'scripts/ops/consensus-prune.py:L101-L112'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L115-L120'
  - symbol: _env_flag
    kind: function
    at: 'scripts/ops/consensus-prune.py:L123-L124'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L127-L128'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L131-L132'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L135-L139'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L142-L149'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L152-L153'
  - symbol: Section
    kind: class
    at: 'scripts/ops/consensus-prune.py:L157-L172'
  - symbol: __init__
    kind: method
    at: 'scripts/ops/consensus-prune.py:L160-L168'
  - symbol: kind
    kind: method
    at: 'scripts/ops/consensus-prune.py:L171-L172'
  - symbol: Removal
    kind: class
    at: 'scripts/ops/consensus-prune.py:L175-L184'
  - symbol: __init__
    kind: method
    at: 'scripts/ops/consensus-prune.py:L179-L184'
  - symbol: _split_sections
    kind: function
    at: 'scripts/ops/consensus-prune.py:L187-L195'
  - symbol: _mark_primary
    kind: function
    at: 'scripts/ops/consensus-prune.py:L198-L219'
  - symbol: flush
    kind: function
    at: 'scripts/ops/consensus-prune.py:L204-L207'
  - symbol: _tail_pass
    kind: function
    at: 'scripts/ops/consensus-prune.py:L223-L227'
  - symbol: _entries_wwd
    kind: function
    at: 'scripts/ops/consensus-prune.py:L230-L262'
  - symbol: _entries_para
    kind: function
    at: 'scripts/ops/consensus-prune.py:L265-L282'
  - symbol: _select
    kind: function
    at: 'scripts/ops/consensus-prune.py:L285-L308'
  - symbol: _line_offsets
    kind: function
    at: 'scripts/ops/consensus-prune.py:L312-L316'
  - symbol: _strip_and_blocks
    kind: function
    at: 'scripts/ops/consensus-prune.py:L319-L334'
  - symbol: _rebuild
    kind: function
    at: 'scripts/ops/consensus-prune.py:L337-L346'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L350-L647'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L379-L395'
  - symbol: after_bytes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L461-L462'
  - symbol: record_history
    kind: function
    at: 'scripts/ops/consensus-prune.py:L478-L495'
  - symbol: emit_warns
    kind: function
    at: 'scripts/ops/consensus-prune.py:L497-L499'
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/ledger-guard.py:L43-L48'
  - symbol: _env_float
    kind: function
    at: 'scripts/ops/ledger-guard.py:L51-L55'
  - symbol: _app
    kind: function
    at: 'scripts/ops/ledger-guard.py:L58-L59'
  - symbol: _find_ledger
    kind: function
    at: 'scripts/ops/ledger-guard.py:L62-L69'
  - symbol: _metrics
    kind: function
    at: 'scripts/ops/ledger-guard.py:L72-L84'
  - symbol: _backup
    kind: function
    at: 'scripts/ops/ledger-guard.py:L87-L101'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/ledger-guard.py:L104-L108'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/ledger-guard.py:L111-L118'
  - symbol: _rebase_after_prune
    kind: function
    at: 'scripts/ops/ledger-guard.py:L125-L142'
  - symbol: _check
    kind: function
    at: 'scripts/ops/ledger-guard.py:L145-L170'
  - symbol: main
    kind: function
    at: 'scripts/ops/ledger-guard.py:L173-L240'
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

Maintenance of the long-lived memory files (consensus.md, candidate-registry.md, operator-requests.md) that the agent reads each cycle. Includes consensus-prune.py (archives old per-cycle entries when file exceeds size threshold to prevent the [PROMPT-SIZE] brake, with a rebuild invariant and SHA-256 verification), registry-archive.py (archives stale registry sections with protected-region byte-identity and compare-and-swap on mtime), ledger-guard.py (post-cycle integrity guard detecting silent content loss via rolling backups and metric comparison), and idle-skip-note.py (records model-free idle-skip events as one line per day).
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
