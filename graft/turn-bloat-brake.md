---
name: turn bloat brake
slug: turn-bloat-brake
type: system
sources:
  - path: scripts/ops/turn-bloat-brake.py
    hash: c4d72b732830311e89db486abb41c8a13a5760ffa043354c953b99a155ff96fb
  - path: tests/test_turn_bloat_brake.py
    hash: 9599b12fa9480d0058872f2facb8d329c5deac8177df794c41982d955d887a74
sources_digest: 9bab211188e6b3ffdbb951a4b1dfcd62caafd3baa64b00f118f99962ad90898b
links:
  - to: turn-economy-audit
    relation: uses
    description: Consumes the BLOATED verdicts produced by turn-audit.
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
  - symbol: newapp
    kind: function
    at: 'tests/test_turn_bloat_brake.py:L15-L18'
  - symbol: rec
    kind: function
    at: 'tests/test_turn_bloat_brake.py:L21-L27'
  - symbol: fb
    kind: function
    at: 'tests/test_turn_bloat_brake.py:L30-L36'
  - symbol: consecutive
    kind: function
    at: 'tests/test_turn_bloat_brake.py:L39-L40'
  - symbol: check
    kind: function
    at: 'tests/test_turn_bloat_brake.py:L43-L46'
---
<!-- context:generated:start -->
## Summary

scripts/ops/turn-bloat-brake.py tracks consecutive BLOATED verdicts per app and triggers an alarm and hard feedback after a configurable streak threshold (default K=3, overridable via TURN_BLOAT_STREAK). The streak increments only on BLOATED, resets on ok/CHATTY, fires exactly once when crossing the threshold, suppresses repeat alarms, and a kill switch (TURN_BLOAT_ENABLED=0) prevents state writes.

## Related

- uses [[turn-economy-audit]] — Consumes the BLOATED verdicts produced by turn-audit.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
