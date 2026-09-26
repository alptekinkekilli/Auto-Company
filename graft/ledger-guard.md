---
name: ledger guard
slug: ledger-guard
type: system
sources:
  - path: scripts/ops/ledger-guard.py
    hash: 9892f74da9b9b06f9977b053a05717c67eeafc4030ee7dbd2e2bc087fb8c3400
  - path: tests/test_ledger_guard.py
    hash: d0118c31c5f02cb01c7ad332056d6ec8c8951338d217999eda93e15dce90a354
sources_digest: 43d871331ac348b9f8d85f7fd50f1ca6129fc137ff6d7ca764693d7af809406c
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
  - symbol: _check
    kind: function
    at: 'scripts/ops/ledger-guard.py:L121-L146'
  - symbol: main
    kind: function
    at: 'scripts/ops/ledger-guard.py:L149-L212'
  - symbol: newapp
    kind: function
    at: 'tests/test_ledger_guard.py:L15-L20'
  - symbol: ledger
    kind: function
    at: 'tests/test_ledger_guard.py:L23-L24'
  - symbol: run
    kind: function
    at: 'tests/test_ledger_guard.py:L27-L33'
  - symbol: body
    kind: function
    at: 'tests/test_ledger_guard.py:L36-L42'
  - symbol: check
    kind: function
    at: 'tests/test_ledger_guard.py:L45-L48'
---
<!-- context:generated:start -->
## Summary

Monitors a ledger file for unexpected section/row/size changes and emits alarms unless an incident note is present; creates first-run backups, rotates backups honoring LEDGER_GUARD_KEEP, and has a kill switch via LEDGER_GUARD_ENABLED=0.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
