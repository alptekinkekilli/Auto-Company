---
name: Work-window & bloat brakes
slug: work-window-bloat-brakes
type: concept
sources:
  - path: scripts/ops/turn-bloat-brake.py
    hash: c4d72b732830311e89db486abb41c8a13a5760ffa043354c953b99a155ff96fb
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
  - path: tests/test_auto_loop_work_window.sh
    hash: 7bb4ebdcaef7c71820540195fab59c8c657ff11f525429105bb0376a30405369
sources_digest: d129f93c6e6e340f890c9ac5c530b28edbc1408dcb6f71bb75eceb52821b1eaf
links:
  - to: state-snapshot-delta-probing
    relation: depends_on
    description: >-
      The work-window brake parses the DELTA line from state-snapshot.py to
      detect surface changes.
  - to: turn-economics-auditing
    relation: depends_on
    description: The bloat brake's BLOATED verdict comes from turn-audit.py's thresholds.
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
---
<!-- context:generated:start -->
## Summary

A cross-cutting fail-closed design: work-window.py opens a K-cycle window when a tracked surface changes (OPREQ resolve, source re-base) so the loop cannot emit a legitimate-but-harmful EMPTY CYCLE confirmation that orphans follow-on work; turn-bloat-brake.py escalates consecutive BLOATED cycles. Both are kill-switchable via env vars, always exit 0 (or fail open to exit 10) so they never kill the harness, and rely on the discretionary-spend cap as the money backstop against a stuck-open window.

## Related

- depends on [[state-snapshot-delta-probing]] — The work-window brake parses the DELTA line from state-snapshot.py to detect surface changes.
- depends on [[turn-economics-auditing]] — The bloat brake's BLOATED verdict comes from turn-audit.py's thresholds.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
