---
name: work window brake
slug: work-window-brake
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

work-window.py is an empty-cycle work-window brake: a changed delta opens the window and records opened_at_cycle and reason; no delta with no state stays closed; fresh window (age < TTL) stays open, expired one closes; restart with negative age fails closed; corrupt state or missing DELTA line fail open; first snapshot is closed; WORK_WINDOW_ENABLED=0 kill switch forces closed; TTL overridable. work-window-watchdog.py is an alarm layer detecting consecutive empty work cycles while the window is open, emitting an alarm only once when crossing threshold (not every violation), with a 'failed' cycle not counted as a violation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
