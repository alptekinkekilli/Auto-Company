---
name: Work-window brake
slug: work-window-brake
type: system
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
  - path: tests/test_work_window.py
    hash: d8c97cca8d25af801fd7214e5176acbe222a9d2ba05610141bf1fd1f40a1bff2
sources_digest: cb541901ab3470155e684d096b907a7cf72c8642b19a774999e0c9803a5d42c1
links:
  - to: auto-loop-harness
    relation: part_of
    description: >-
      Wired into auto-loop.sh: _workwin_open gates idle-skip and the window exit
      code is captured set-e-safe.
  - to: state-snapshot
    relation: uses
    description: >-
      work-window.py parses the DELTA: line emitted by state-snapshot.py to
      decide whether to open/extend the window.
generator:
  version: 1
covers:
  - symbol: file_sha16
    kind: function
    at: 'scripts/ops/state-snapshot.py:L54-L61'
  - symbol: directive_state
    kind: function
    at: 'scripts/ops/state-snapshot.py:L64-L72'
  - symbol: opreq_open
    kind: function
    at: 'scripts/ops/state-snapshot.py:L75-L87'
  - symbol: wowcar_sources
    kind: function
    at: 'scripts/ops/state-snapshot.py:L90-L104'
  - symbol: main
    kind: function
    at: 'scripts/ops/state-snapshot.py:L107-L166'
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
  - symbol: run
    kind: function
    at: 'tests/test_work_window.py:L21-L42'
  - symbol: check
    kind: function
    at: 'tests/test_work_window.py:L45-L48'
---
<!-- context:generated:start -->
## Summary

A fail-closed brake preventing the harness from emitting legitimate-but-harmful EMPTY CYCLE confirmations when a tracked surface change leaves follow-on work orphaned. It reads the state-snapshot DELTA line, maintains a K-cycle window in logs/work-window.json, fails open (exit 10) on corrupt state, and relies on the discretionary-spend cap as the money backstop against a stuck-open window. The watchdog alarm companion fires only on narrow EMPTY_RE phrasings, never generic 'blocked' words.

## Related

- part of [[auto-loop-harness]] — Wired into auto-loop.sh: _workwin_open gates idle-skip and the window exit code is captured set-e-safe.
- uses [[state-snapshot]] — work-window.py parses the DELTA: line emitted by state-snapshot.py to decide whether to open/extend the window.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
