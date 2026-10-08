---
name: ledger guard
slug: ledger-guard
type: system
sources:
  - path: tests/test_ledger_guard.py
    hash: d0118c31c5f02cb01c7ad332056d6ec8c8951338d217999eda93e15dce90a354
sources_digest: c31506ce3d2e2d56dcdf4e093db6e7929c46cc4bcff6990a198461be0541b5c3
links: []
generator:
  version: 1
covers:
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

ledger-guard.py monitors a ledger file for unexpected changes (section/row count, size) and emits alarms unless an incident note is present. It creates a backup on first run, stays silent on unchanged state, honors LEDGER_GUARD_KEEP for backup rotation, and has a kill switch via LEDGER_GUARD_ENABLED=0. Missing-file detection and incident: marker exemption are covered.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
