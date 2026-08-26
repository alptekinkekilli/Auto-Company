---
name: threshold pinning against drift
slug: threshold-pinning-against-drift
type: concept
sources:
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: d172c81ad96a0a7833800c32917ff357b620817a9ca217cba878f3d6f8500ea3
links:
  - to: turn-audit-policy-engine
    relation: configures
    description: >-
      The pinned boundary values define the verdict thresholds the engine
      applies.
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

Turn-economy verdict thresholds are pinned to explicit boundary values (55 vs 56 turns, 66 turns, duration-based bloating) so silent recalibration drift is caught. Comments document the rationale behind the recalibrated bars (p80/p90, watchdog proximity, cost) to guide future changes.

## Related

- configures [[turn-audit-policy-engine]] — The pinned boundary values define the verdict thresholds the engine applies.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
