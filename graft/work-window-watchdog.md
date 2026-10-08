---
name: work window watchdog
slug: work-window-watchdog
type: system
sources:
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: tests/test_work_window_watchdog.py
    hash: 43cd4a904f4badbb8ce3a4ee88adff57b790ff6c8067435e361617f37a10de40
sources_digest: b299afbc28e7c74d221a99c8d8786bdf203e494016527d928a64c829a29f6ef0
links:
  - to: work-window-brake
    relation: uses
    description: The watchdog layers on top of the work-window state.
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
  - symbol: run
    kind: function
    at: 'tests/test_work_window_watchdog.py:L18-L29'
  - symbol: check
    kind: function
    at: 'tests/test_work_window_watchdog.py:L32-L35'
---
<!-- context:generated:start -->
## Summary

scripts/ops/work-window-watchdog.py is an alarm layer detecting consecutive empty work cycles while the work window is open. It emits an alarm only once when the consecutive count crosses the threshold (default overridable via WORK_WINDOW_WATCHDOG_THRESHOLD), not on every subsequent violation, resets on real work, and does not count a 'failed' cycle as a violation. An escape clause covers enumerated blockers.

## Related

- uses [[work-window-brake]] — The watchdog layers on top of the work-window state.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
