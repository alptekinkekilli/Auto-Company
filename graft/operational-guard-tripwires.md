---
name: Operational guard tripwires
slug: operational-guard-tripwires
type: system
sources:
  - path: scripts/ops/turn-bloat-brake.py
    hash: c4d72b732830311e89db486abb41c8a13a5760ffa043354c953b99a155ff96fb
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 82fd9dfa80c4f0c916c506e6a44db71dbfd6ee1c0421bcedf8d255b77c3bfd7e
  - path: tests/test_auto_loop_ledger_guard.sh
    hash: 707a207723f0b5c371c39d0fbc5a14170b4c74bb9c893f550186797aebcf440f
  - path: tests/test_auto_loop_work_window.sh
    hash: 7bb4ebdcaef7c71820540195fab59c8c657ff11f525429105bb0376a30405369
  - path: tests/test_consensus_prune.py
    hash: 19b42032e177c12e1838357377be54792d7044f49da71bf4c97a539ff11e4da4
sources_digest: 82f07a94342a4a49ced8f0f604cead0b51c82580cd51d6f828ad7ed5b0a1dce0
links:
  - to: auto-loop-harness-budget-governance
    relation: part_of
    description: >-
      These guards are invoked from auto-loop.sh at specific points in the
      cycle.
  - to: state-snapshot-delta-probing
    relation: uses
    description: >-
      work-window.py reads the DELTA line emitted by state-snapshot.py to decide
      whether a surface changed.
  - to: turn-economics-auditing
    relation: uses
    description: turn-bloat-brake consumes the BLOATED verdict produced by turn-audit.py.
generator:
  version: 1
covers:
  - symbol: _app
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L25-L26'
  - symbol: _streak_len
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L29-L34'
  - symbol: _load
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L37-L41'
  - symbol: _save
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L44-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L63-L104'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L45-L48'
  - symbol: _threshold
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L51-L57'
  - symbol: _read_state
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L60-L64'
  - symbol: _write_state
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L67-L74'
  - symbol: main
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L77-L125'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/work-window.py:L44-L48'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/work-window.py:L51-L58'
  - symbol: _parse_delta
    kind: function
    at: 'scripts/ops/work-window.py:L61-L70'
  - symbol: _read_state
    kind: function
    at: 'scripts/ops/work-window.py:L73-L80'
  - symbol: _write_state
    kind: function
    at: 'scripts/ops/work-window.py:L83-L87'
  - symbol: _line
    kind: function
    at: 'scripts/ops/work-window.py:L90-L100'
  - symbol: main
    kind: function
    at: 'scripts/ops/work-window.py:L103-L160'
  - symbol: check
    kind: function
    at: 'tests/test_consensus_prune.py:L17-L20'
  - symbol: newapp
    kind: function
    at: 'tests/test_consensus_prune.py:L23-L26'
  - symbol: consensus
    kind: function
    at: 'tests/test_consensus_prune.py:L29-L30'
  - symbol: entry
    kind: function
    at: 'tests/test_consensus_prune.py:L33-L38'
  - symbol: doc
    kind: function
    at: 'tests/test_consensus_prune.py:L41-L51'
  - symbol: run
    kind: function
    at: 'tests/test_consensus_prune.py:L54-L62'
  - symbol: guard
    kind: function
    at: 'tests/test_consensus_prune.py:L65-L68'
---
<!-- context:generated:start -->
## Summary

A family of fail-closed Python guards wired into auto-loop.sh that prevent harmful or unplanned behavior: ledger-guard.py (incident detection), consensus-prune.py (archives stale consensus entries, deduped by SHA, must not trip the incident regex), work-window.py (blocks empty-cycle confirmations when a tracked surface change leaves orphaned work), turn-bloat-brake.py (escalates consecutive BLOATED cycles to a hard mandate), and work-window-watchdog.py (alarms on repeated empty confirmations). All are advisory or fail-closed, never fail the loop, and write state atomically via tmp+rename.

## Related

- part of [[auto-loop-harness-budget-governance]] — These guards are invoked from auto-loop.sh at specific points in the cycle.
- uses [[state-snapshot-delta-probing]] — work-window.py reads the DELTA line emitted by state-snapshot.py to decide whether a surface changed.
- uses [[turn-economics-auditing]] — turn-bloat-brake consumes the BLOATED verdict produced by turn-audit.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
