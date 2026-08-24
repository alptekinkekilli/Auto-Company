---
name: turn-audit policy script
slug: turn-audit-policy-script
type: file
sources:
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
sources_digest: 2fc4aebe6ed034f35677032d3c0cd8e6724061b52cd35d532127ff86bf888892
links:
  - to: turn-audit-regression-suite
    relation: validates
    description: >-
      The test suite pins boundary values (55/56 turns, 66 turns, duration-based
      bloating) and asserts verdict thresholds and --summary-last behavior to
      prevent silent recalibration drift.
generator:
  version: 1
covers:
  - symbol: ts_of
    kind: function
    at: 'scripts/ops/turn-audit.py:L74-L78'
  - symbol: scan
    kind: function
    at: 'scripts/ops/turn-audit.py:L81-L112'
  - symbol: floor_usd
    kind: function
    at: 'scripts/ops/turn-audit.py:L115-L118'
  - symbol: summary_line
    kind: function
    at: 'scripts/ops/turn-audit.py:L121-L139'
  - symbol: main
    kind: function
    at: 'scripts/ops/turn-audit.py:L142-L155'
---
<!-- context:generated:start -->
## Summary

Implements the turn-economy policy (section 4): parses daily log lines, counts turns/messages per session, accounts for cache usage, and classifies sessions as CHATTY/BLOATED/ok against recalibrated thresholds (p80/p90, watchdog proximity, cost). Supports a --summary-last flag that selects the newest session.

## Related

- validates [[turn-audit-regression-suite]] — The test suite pins boundary values (55/56 turns, 66 turns, duration-based bloating) and asserts verdict thresholds and --summary-last behavior to prevent silent recalibration drift.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
