---
name: Content-hash provenance
slug: content-hash-provenance
type: concept
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
  - path: scripts/ops/consensus-prune.py
    hash: 8f4770cc811cb6df649d8003446b2ce59125e8ee2482fc513a9f59a2303a8400
  - path: scripts/ops/kik-decision-read.py
    hash: 4f2060cbaaa784433de9720f1e9a3bfb3ba6c06cab00fae0efa0a426e5c926de
  - path: scripts/ops/ledger-guard.py
    hash: 5b3098424eada1d1f669995baf5e1dd76ea4fb724c0c524ddc9986ce361128d7
sources_digest: dc63e10df81c2f256a280993b32dcd7d8ebfd57ea951b76f677ebe98ea5f5d4d
links: []
generator:
  version: 1
covers:
  - symbol: normalize
    kind: function
    at: 'scripts/core/decision_text_hash.py:L54-L60'
  - symbol: digest
    kind: function
    at: 'scripts/core/decision_text_hash.py:L63-L65'
  - symbol: fetch
    kind: function
    at: 'scripts/core/decision_text_hash.py:L68-L96'
  - symbol: main
    kind: function
    at: 'scripts/core/decision_text_hash.py:L99-L112'
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
  - symbol: _hasher
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L45-L51'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L54-L67'
  - symbol: text_of
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L70-L73'
  - symbol: first
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L76-L78'
  - symbol: field
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L81-L89'
  - symbol: read
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L92-L131'
  - symbol: main
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L134-L159'
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

Cross-cutting invariant that content hashes must be produced by exactly one canonical implementation to be comparable. decision_text_hash.py is the single source of truth for KİK decision pages (raw HTML varies by client), and kik-decision-read.py dynamically imports it to guarantee comparability with the bridge's recorded value. A hash produced any other way is not comparable and must not be written to the bridge — a lesson from a 2026-07-29 incident where an underdetermined spec caused a legitimate evidence quarantine. The same sha16/sha256 discipline appears in ledger-guard and consensus-prune for idempotency and loss detection.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
