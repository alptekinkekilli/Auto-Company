---
name: ledger guard & state snapshot
slug: ledger-guard-state-snapshot
type: system
sources:
  - path: tests/test_ledger_guard.py
    hash: d0118c31c5f02cb01c7ad332056d6ec8c8951338d217999eda93e15dce90a354
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: 01d27662926b30dbbb4d7fafb4a46f4c4a14f9ae08f8fe69d3e1f00c61ab61e6
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

scripts/ops/ledger-guard.py monitors a ledger file for unexpected section/row-count/size changes and emits alarms unless an incident note is present, with first-run backup creation, backup rotation honoring LEDGER_GUARD_KEEP, and a kill switch. state-snapshot.py computes DELTA change-detection over local fields (all fields local since a 2026-08-24 re-charter; bridge/send/reply retired), excluding errored fields from the next DELTA and exiting 0 even on a missing ledger.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
