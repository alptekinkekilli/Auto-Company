---
name: work window brake
slug: work-window-brake
type: system
sources:
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
  - path: tests/test_work_window.py
    hash: d8c97cca8d25af801fd7214e5176acbe222a9d2ba05610141bf1fd1f40a1bff2
sources_digest: b5ad6294bf5ac92213d2d7c3942ca16fc3a911ddbe3612e5e01747c6e56761b8
links: []
generator:
  version: 1
covers:
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
  - symbol: run
    kind: function
    at: 'tests/test_work_window.py:L21-L42'
  - symbol: check
    kind: function
    at: 'tests/test_work_window.py:L45-L48'
---
<!-- context:generated:start -->
## Summary

scripts/ops/work-window.py is the empty-cycle work-window brake: a changed DELTA opens the window (recording opened_at_cycle and reason), no delta with no state stays closed, a fresh window (age < TTL) stays open, an expired one closes, a restart with negative age fails closed, corrupt state or missing DELTA line fails open, and the first snapshot is closed. WORK_WINDOW_ENABLED=0 forces closed; TTL overridable via WORK_WINDOW_TTL_CYCLES.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
