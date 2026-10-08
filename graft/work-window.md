---
name: work window
slug: work-window
type: system
sources:
  - path: tests/test_work_window.py
    hash: d8c97cca8d25af801fd7214e5176acbe222a9d2ba05610141bf1fd1f40a1bff2
sources_digest: e9d0e4b69919e1811eabb8fb540ea206ef2aff4b6cd425036b445ffb82245794
links:
  - to: state-snapshot-and-delta
    relation: uses
    description: Consumes DELTA lines to decide open/closed
  - to: work-window-watchdog
    relation: uses
    description: The watchdog layers on top of the work window
generator:
  version: 1
covers:
  - symbol: run
    kind: function
    at: 'tests/test_work_window.py:L21-L42'
  - symbol: check
    kind: function
    at: 'tests/test_work_window.py:L45-L48'
---
<!-- context:generated:start -->
## Summary

work-window.py is the empty-cycle work-window brake: a changed DELTA opens the window and records opened_at_cycle and reason; no delta with no state stays closed; a fresh window (age < TTL) stays open, an expired one closes; a restart with negative age (stored opened_at_cycle > current cycle) fails closed; corrupt state or missing DELTA line fail open; the first snapshot is closed; WORK_WINDOW_ENABLED=0 forces closed; TTL overridable via WORK_WINDOW_TTL_CYCLES. Exit code 10 = open, 0 = closed.

## Related

- uses [[state-snapshot-and-delta]] — Consumes DELTA lines to decide open/closed
- uses [[work-window-watchdog]] — The watchdog layers on top of the work window
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
