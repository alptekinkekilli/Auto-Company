---
name: discretionary budget
slug: discretionary-budget
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
sources_digest: ed00c40387506c9a1c4ffdd3e1d146bd9bbdafb68e37d52bbfb034ffa9ffae6e
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The cap injection and idle detection live in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A discretionary daily cap injects a warning line into the prompt once the day's spend reaches a threshold (default $30, 3600s idle interval). The ledger is discretionary-spend.ndjson; the sum skips malformed lines and returns 0.00 on a missing file, and the cap comparison uses >= so an exact match triggers. The idle check fails open. Exactly two injection sites exist (one per prompt branch).

## Related

- part of [[auto-loop-core-engine]] — The cap injection and idle detection live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
