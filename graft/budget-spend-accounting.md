---
name: Budget & spend accounting
slug: budget-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
sources_digest: 9acc0249ddcf7d53dc97c65117d01ec63059f34e1003f3864d7b48ce6de9355a
links:
  - to: auto-loop-core-auto-loop-sh
    relation: part_of
    description: Functions live in auto-loop.sh and are exercised by budget-gate tests.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Measures and gates spend from two disjoint sources (ccusage CLI sessions + TOTAL_SPEND_LEDGER rows) summed, never maxed, to avoid vanishing real spend. Fail-closed: degraded reads never lower a same-period prior observation, first-ever failure latches a hold returning NA. Weekly resume-time walk counts codex ledger rows; malformed amounts abort conservatively.

## Related

- part of [[auto-loop-core-auto-loop-sh]] — Functions live in auto-loop.sh and are exercised by budget-gate tests.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
