---
name: Turn Bloat Escalation
slug: turn-bloat-escalation
type: system
sources:
  - path: scripts/ops/turn-bloat-brake.py
    hash: c4d72b732830311e89db486abb41c8a13a5760ffa043354c953b99a155ff96fb
  - path: tests/test_auto_loop_ledger_guard.sh
    hash: 707a207723f0b5c371c39d0fbc5a14170b4c74bb9c893f550186797aebcf440f
sources_digest: fce482ee58c875edd26b6e5d7f743384f451c7ae0d3a6c5f9a605144e910fae6
links:
  - to: auto-loop-harness
    relation: part_of
    description: Wired into scripts/core/auto-loop.sh as a post-cycle guard
  - to: cycle-economics-cost-auditing
    relation: uses
    description: Consumes the BLOATED verdict produced by turn-audit.py
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
---
<!-- context:generated:start -->
## Summary

Operational escalation for bloated cycles: turn-bloat-brake.py tracks consecutive BLOATED cycles (turns>65, dur>=675s, cost>=$5) and emits a hard mandate once a streak crosses a threshold, complementing the softer per-cycle advisory from turn-audit. It always exits 0 so it never fails the harness loop, resets the streak on any non-BLOATED verdict, and stays quiet after the crossing alarm to avoid spam. The HARD_LINE mandate (persist one milestone, end immediately) is printed pre-cycle when a streak is active.

## Related

- part of [[auto-loop-harness]] — Wired into scripts/core/auto-loop.sh as a post-cycle guard
- uses [[cycle-economics-cost-auditing]] — Consumes the BLOATED verdict produced by turn-audit.py
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
