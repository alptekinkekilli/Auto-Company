---
name: Consensus & ledger integrity guards
slug: consensus-ledger-integrity-guards
type: system
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 8f4770cc811cb6df649d8003446b2ce59125e8ee2482fc513a9f59a2303a8400
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/ledger-guard.py
    hash: 5b3098424eada1d1f669995baf5e1dd76ea4fb724c0c524ddc9986ce361128d7
sources_digest: afa66eee65f35fd181ddd75c6b550fd352ac6491d0bf0b819d753a498a2d1436
links:
  - to: auto-loop-orchestration
    relation: uses
    description: >-
      ledger-guard runs after each cycle; consensus-prune prevents the
      [PROMPT-SIZE] brake from firing every cycle.
  - to: content-hash-provenance
    relation: implements
    description: Both use sha16/sha256 hashes for idempotency and loss detection.
generator:
  version: 1
covers:
  - symbol: _load_runtime_env
    kind: function
    at: 'scripts/ops/consensus-prune.py:L64-L75'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L78-L83'
  - symbol: _env_flag
    kind: function
    at: 'scripts/ops/consensus-prune.py:L86-L87'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L90-L91'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L94-L95'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L98-L102'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L105-L112'
  - symbol: _section_sizes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L115-L120'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L123-L124'
  - symbol: _split_section
    kind: function
    at: 'scripts/ops/consensus-prune.py:L127-L141'
  - symbol: _parse_entries
    kind: function
    at: 'scripts/ops/consensus-prune.py:L144-L174'
  - symbol: _check_monotonic
    kind: function
    at: 'scripts/ops/consensus-prune.py:L177-L184'
  - symbol: _archive_path
    kind: function
    at: 'scripts/ops/consensus-prune.py:L187-L188'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L191-L361'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L215-L233'
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
---
<!-- context:generated:start -->
## Summary

Post-cycle integrity machinery for consensus.md and the Gate-0 conflict ledger, created after an audit revealed silent content loss. ledger-guard.py does rolling backups (LEDGER_GUARD_KEEP default 15) and loss detection comparing section headers, OPEX row references, byte size, SHA-16 against previous cycle state, always exiting 0 and suppressing alarms when an incident marker regex matches (documented repairs); _rebase_after_prune reconciles baselines after consensus-prune.py legitimately reduces the file. consensus-prune.py trims old cycle entries byte-exact into monthly archives with sha256-stamped headers, validates strictly monotonic cycle numbers, keeps KEEP largest (default 8), and alarms on the third consecutive skip while over threshold. idle-skip-note.py records model-free idle-skip events as one line per UTC day so the IDLE-SKIP path leaves an auditable trace without bloating the prompt.

## Related

- uses [[auto-loop-orchestration]] — ledger-guard runs after each cycle; consensus-prune prevents the [PROMPT-SIZE] brake from firing every cycle.
- implements [[content-hash-provenance]] — Both use sha16/sha256 hashes for idempotency and loss detection.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
