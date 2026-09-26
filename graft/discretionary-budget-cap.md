---
name: discretionary budget cap
slug: discretionary-budget-cap
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
sources_digest: 70de1389400068ba03aba538345cb46bca9618dd74a210ce994324fa657c1a37
links:
  - to: auto-loop-core-engine
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A discretionary daily cap injects a warning line into the prompt once the day's spend reaches a threshold, using a 3600s idle interval default, a $30 cap default, and a >= comparison so an exact match triggers the warning; the ledger sum ignores non-JSON lines and missing files.

## Related

- part of [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
