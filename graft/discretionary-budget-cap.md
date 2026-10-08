---
name: discretionary budget cap
slug: discretionary-budget-cap
type: concept
sources:
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
sources_digest: 62ecf9826e8ee0e90ec861065f7d213575d9326c4b34ca2b9c4d42e24b0475af
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The cap logic and injection sites live in auto-loop.sh
  - to: prompt-assembly-contract
    relation: produces
    description: The cap warning line is injected into the assembled prompt
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A discretionary daily cap injects a warning line into the prompt once the day's spend reaches a threshold (default $30, 3600s idle interval). The ledger discretionary-spend.ndjson is summed for today's UTC date, skipping malformed lines and missing files (returns 0.00). The cap comparison uses >= so an exact match triggers the warning, and there are exactly two injection sites (one per prompt branch).

## Related

- part of [[auto-loop-core-engine]] — The cap logic and injection sites live in auto-loop.sh
- produces [[prompt-assembly-contract]] — The cap warning line is injected into the assembled prompt
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
