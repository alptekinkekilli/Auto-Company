---
name: Consensus Pruning and Ledger Guard
slug: consensus-pruning-and-ledger-guard
type: system
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 1a741019d9b78a90dc9121e012850f5bcebd88fbd8527a8b17a4357068ca4684
  - path: scripts/ops/ledger-guard.py
    hash: 5b3098424eada1d1f669995baf5e1dd76ea4fb724c0c524ddc9986ce361128d7
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 9d97a8dfec49f5829637619f996e57ab7e0773498a9788855dacc61a10d51375
  - path: tests/test_consensus_prune.py
    hash: 4104c6c0b8293637bbdf9f786cfdce8074d8f1353149932bdb5e989bac71e999
sources_digest: 8881a08ff6684e858d280c521f146d0730b35123ca4657f1a19bcfdb555697ec
links:
  - to: auto-loop-harness-brakes-and-guards
    relation: part_of
    description: Prune hook is invoked by auto-loop.sh after ledger-guard.py
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
  - symbol: check
    kind: function
    at: 'tests/test_consensus_prune.py:L24-L27'
  - symbol: skip
    kind: function
    at: 'tests/test_consensus_prune.py:L30-L31'
  - symbol: newapp
    kind: function
    at: 'tests/test_consensus_prune.py:L34-L37'
  - symbol: consensus
    kind: function
    at: 'tests/test_consensus_prune.py:L40-L41'
  - symbol: entry
    kind: function
    at: 'tests/test_consensus_prune.py:L44-L49'
  - symbol: para
    kind: function
    at: 'tests/test_consensus_prune.py:L52-L56'
  - symbol: doc
    kind: function
    at: 'tests/test_consensus_prune.py:L59-L70'
  - symbol: doc2
    kind: function
    at: 'tests/test_consensus_prune.py:L73-L95'
  - symbol: run
    kind: function
    at: 'tests/test_consensus_prune.py:L101-L110'
  - symbol: guard
    kind: function
    at: 'tests/test_consensus_prune.py:L113-L116'
  - symbol: headers
    kind: function
    at: 'tests/test_consensus_prune.py:L119-L120'
  - symbol: section
    kind: function
    at: 'tests/test_consensus_prune.py:L123-L127'
  - symbol: non_cycle_paras
    kind: function
    at: 'tests/test_consensus_prune.py:L130-L131'
  - symbol: archive_pieces
    kind: function
    at: 'tests/test_consensus_prune.py:L134-L149'
  - symbol: full
    kind: function
    at: 'tests/test_consensus_prune.py:L366-L368'
---
<!-- context:generated:start -->
## Summary

Maintenance of the canonical consensus document and the operational ledger: consensus-prune.py prunes old entries while archiving them byte-exactly to docs/operations/consensus-archive-*.md (threshold 70,000 bytes, per-section caps, kill switches, streak-based alarms), and ledger-guard.py guards the operational ledger. The prune hook is wired into auto-loop.sh after ledger-guard.py, gated on cycle_failed_reason being empty.

## Related

- part of [[auto-loop-harness-brakes-and-guards]] — Prune hook is invoked by auto-loop.sh after ledger-guard.py
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
