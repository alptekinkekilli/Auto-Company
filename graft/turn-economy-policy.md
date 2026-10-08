---
name: turn economy policy
slug: turn-economy-policy
type: system
sources:
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
  - path: tests/test_turn_bloat_brake.py
    hash: 9599b12fa9480d0058872f2facb8d329c5deac8177df794c41982d955d887a74
sources_digest: 2e94fa5b7b9400debe79e6c573c421ac60369358f27f55e7554a08b1a2377a5e
links:
  - to: auto-loop-core-engine
    relation: uses
    description: Turn verdicts feed the loop's turn-feedback slot in the prompt
generator:
  version: 1
covers:
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

turn-audit.py implements the turn-economy policy (section 4): session parsing, turn/message counting, cache accounting, and verdict thresholds (CHATTY, BLOATED, ok) with --summary-last selecting the newest session. Boundary values (55 vs 56 turns, 66 turns, duration-based bloating) are pinned to prevent silent recalibration drift; bars are calibrated at p80/p90 with watchdog proximity and cost in mind. turn-bloat-brake.py tracks consecutive BLOATED verdicts per app and triggers an alarm and hard feedback after a configurable streak threshold (default K=3, overridable via TURN_BLOAT_STREAK), resetting on ok/CHATTY, with a kill switch TURN_BLOAT_ENABLED=0.

## Related

- uses [[auto-loop-core-engine]] — Turn verdicts feed the loop's turn-feedback slot in the prompt
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
