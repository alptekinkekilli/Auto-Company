---
name: Budget and spend accounting
slug: budget-and-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 8047ae1ceb7eac76beba89e0584912e2500baee4f68bb2f372c872739a2c7193
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
sources_digest: f2c363d2e7312777847782b14ec618169fc836259077418d91f416415cc81fd1
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Budget functions are extracted from auto-loop.sh and tested in isolation.
  - to: state-snapshot-probe
    relation: uses
    description: 'Discretionary budget uses the snapshot DELTA:none idle signal.'
generator:
  version: 1
covers:
  - symbol: is_web
    kind: function
    at: 'scripts/ops/web-research-cost.py:L43-L44'
  - symbol: analyse
    kind: function
    at: 'scripts/ops/web-research-cost.py:L47-L76'
  - symbol: main
    kind: function
    at: 'scripts/ops/web-research-cost.py:L79-L161'
---
<!-- context:generated:start -->
## Summary

The fail-closed spend measurement and budget-gate logic in auto-loop.sh: ccusage reads, codex ledger summation, period resets, and the discretionary daily cap. Degraded reads never lower a same-period prior observation, and unmeasured cycles latch a hold.

## Related

- part of [[auto-loop-core-engine]] — Budget functions are extracted from auto-loop.sh and tested in isolation.
- uses [[state-snapshot-probe]] — Discretionary budget uses the snapshot DELTA:none idle signal.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
