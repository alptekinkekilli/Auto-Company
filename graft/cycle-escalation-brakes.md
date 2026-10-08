---
name: Cycle Escalation Brakes
slug: cycle-escalation-brakes
type: system
sources:
  - path: scripts/ops/turn-bloat-brake.py
    hash: c4d72b732830311e89db486abb41c8a13a5760ffa043354c953b99a155ff96fb
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
  - path: tests/test_auto_loop_ledger_guard.sh
    hash: 707a207723f0b5c371c39d0fbc5a14170b4c74bb9c893f550186797aebcf440f
  - path: tests/test_auto_loop_work_window.sh
    hash: 7bb4ebdcaef7c71820540195fab59c8c657ff11f525429105bb0376a30405369
sources_digest: e92424718c3880e8347eb85bd56e349877890071a2771ab2015ee5bb23ec8f4d
links:
  - to: cycle-economics-auditing
    relation: depends_on
    description: >-
      turn-bloat-brake.py consumes turn-audit.py's BLOATED verdicts;
      work-window.py consumes the state-snapshot DELTA line.
  - to: state-snapshot-consensus
    relation: uses
    description: >-
      work-window.py reads the state-snapshot DELTA line on stdin; the watchdog
      points to memories/consensus.md and the conflict ledger for judgment.
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

Operational escalation and brake scripts that prevent the auto-loop harness from emitting harmful confirmations or burning budget. turn-bloat-brake.py tracks consecutive BLOATED cycles and emits a hard mandate (persist one milestone, end immediately) once a streak crosses a threshold, resetting on any non-BLOATED verdict. work-window.py is a fail-closed brake that prevents EMPTY CYCLE confirmations when a tracked surface change leaves follow-on work orphaned, keeping a K-cycle window and failing open (exit 10) on corrupt state. work-window-watchdog.py detects empty-cycle confirmations while a window is open and alarms after a threshold, using deliberately narrow regex phrasings because the brake's escape clause requires enumerating blocked items. All always exit 0 (or 10) so they never fail the harness loop, and write state atomically via temp+rename.

## Related

- depends on [[cycle-economics-auditing]] — turn-bloat-brake.py consumes turn-audit.py's BLOATED verdicts; work-window.py consumes the state-snapshot DELTA line.
- uses [[state-snapshot-consensus]] — work-window.py reads the state-snapshot DELTA line on stdin; the watchdog points to memories/consensus.md and the conflict ledger for judgment.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
