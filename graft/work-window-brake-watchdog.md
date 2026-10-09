---
name: Work-Window Brake & Watchdog
slug: work-window-brake-watchdog
type: system
sources:
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
  - path: tests/test_auto_loop_work_window.sh
    hash: 7bb4ebdcaef7c71820540195fab59c8c657ff11f525429105bb0376a30405369
sources_digest: 018327e9f5bfa9b608840268a3baab5c8fbfc5e07b656469982956b950619b56
links:
  - to: auto-loop-harness
    relation: part_of
    description: >-
      Wired into scripts/core/auto-loop.sh; relies on the discretionary-spend
      cap as money backstop against a stuck-open window
  - to: state-snapshot-probe
    relation: uses
    description: 'Reads the state-snapshot block on stdin and parses the DELTA: line'
generator:
  version: 1
covers:
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
---
<!-- context:generated:start -->
## Summary

A fail-closed brake preventing the auto-loop harness from emitting legitimate-but-harmful EMPTY CYCLE confirmations when a tracked surface change leaves follow-on work orphaned. work-window.py reads the state-snapshot DELTA line, maintains a K-cycle window in logs/work-work-window.json, and fails open (exit 10) on unparseable/corrupt state. The companion watchdog detects empty-cycle confirmations while a window is open and alarms after consecutive occurrences, using deliberately narrow phrasings because the brake's escape clause requires enumerating blocked items.

## Related

- part of [[auto-loop-harness]] — Wired into scripts/core/auto-loop.sh; relies on the discretionary-spend cap as money backstop against a stuck-open window
- uses [[state-snapshot-probe]] — Reads the state-snapshot block on stdin and parses the DELTA: line
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
