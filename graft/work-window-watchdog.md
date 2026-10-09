---
name: work window & watchdog
slug: work-window-watchdog
type: system
sources:
  - path: tests/test_work_window_watchdog.py
    hash: 43cd4a904f4badbb8ce3a4ee88adff57b790ff6c8067435e361617f37a10de40
  - path: tests/test_work_window.py
    hash: d8c97cca8d25af801fd7214e5176acbe222a9d2ba05610141bf1fd1f40a1bff2
sources_digest: 6dfb4eb33d5e7c7ee8841a9b89922ac9763145071265d0b39d705106ef95fb77
links: []
generator:
  version: 1
covers:
  - symbol: run
    kind: function
    at: 'tests/test_work_window.py:L21-L42'
  - symbol: check
    kind: function
    at: 'tests/test_work_window.py:L45-L48'
  - symbol: run
    kind: function
    at: 'tests/test_work_window_watchdog.py:L18-L29'
  - symbol: check
    kind: function
    at: 'tests/test_work_window_watchdog.py:L32-L35'
---
<!-- context:generated:start -->
## Summary

scripts/ops/work-window.py is the empty-cycle work-window brake: a changed DELTA opens the window recording opened_at_cycle and reason, a fresh window (age < TTL) stays open, expired closes, restart with negative age fails closed, corrupt state/missing DELTA fail open, and a kill switch forces closed. work-window-watchdog.py is an alarm layer detecting consecutive empty cycles while the window is open, emitting an alarm only once on crossing the threshold (not every violation), with a failed cycle not counted as a violation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
