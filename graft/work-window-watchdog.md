---
name: work window watchdog
slug: work-window-watchdog
type: concept
sources:
  - path: tests/test_work_window_watchdog.py
    hash: 43cd4a904f4badbb8ce3a4ee88adff57b790ff6c8067435e361617f37a10de40
sources_digest: 0768dd7c4ed814ff418d16d853f796146ba8dd980f93c84ba990443008f1f8b3
links:
  - to: work-window
    relation: uses
    description: Layers on top of the work-window open/closed state
generator:
  version: 1
covers:
  - symbol: run
    kind: function
    at: 'tests/test_work_window_watchdog.py:L18-L29'
  - symbol: check
    kind: function
    at: 'tests/test_work_window_watchdog.py:L32-L35'
---
<!-- context:generated:start -->
## Summary

work-window-watchdog.py detects consecutive empty work cycles while the work window is open and emits an alarm only once when the consecutive count crosses the threshold (default overridable via WORK_WINDOW_WATCHDOG_THRESHOLD), not on every subsequent violation. A 'failed' cycle is not counted as a violation; the escape clause for enumerated blockers resets the counter.

## Related

- uses [[work-window]] — Layers on top of the work-window open/closed state
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
