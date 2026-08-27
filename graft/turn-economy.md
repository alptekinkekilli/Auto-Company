---
name: turn-economy
slug: turn-economy
type: system
sources:
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: d172c81ad96a0a7833800c32917ff357b620817a9ca217cba878f3d6f8500ea3
links:
  - to: auto-loop
    relation: validates
    description: turn-audit.py audits the turn-feedback slot produced by auto-loop.sh.
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

Implements the turn-economy policy (section 4): parses daily logs, counts turns/messages, accounts for cache, and applies verdict thresholds (CHATTY, BLOATED, ok) with --summary-last selecting the newest session. Boundary values (55 vs 56 turns, 66 turns, duration-based bloating) are pinned to prevent silent recalibration drift; bars were recalibrated to p80/p90 with watchdog proximity and cost in mind.

## Related

- validates [[auto-loop]] — turn-audit.py audits the turn-feedback slot produced by auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
