---
name: Ledger integrity guard
slug: ledger-integrity-guard
type: file
sources:
  - path: scripts/ops/ledger-guard.py
    hash: 5b3098424eada1d1f669995baf5e1dd76ea4fb724c0c524ddc9986ce361128d7
sources_digest: 84864fc2941c2156105255a901608e5ef24d0956cb977c82d01d9bb70567455a
links: []
generator:
  version: 1
covers:
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

Post-cycle integrity guard for the Gate-0 conflict ledger and consensus.md, created after an audit revealed silent content loss. Performs rolling backups (retaining last N) and loss detection by comparing current metrics (section headers, OPEX row refs, byte size, SHA-16) against the previous cycle's state. Always exits 0, never failing the orchestration loop, and suppresses alarms when an incident marker regex matches (documented repairs). _rebase_after_prune reconciles baselines after consensus-prune legitimately reduces the file, and files that disappear entirely keep alarming until restored.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
