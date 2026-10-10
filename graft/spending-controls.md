---
name: spending controls
slug: spending-controls
type: system
sources:
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 876da2627d2b04ac153602cb08a700c6c453d5779c9b43bc922fc9550a3b9fd6
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Idle detection and discretionary cap logic live in auto-loop.sh
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Two spending-control mechanisms in auto-loop.sh: idle detection based on snapshot text 'DELTA: none', and a discretionary daily cap that injects a warning line into the prompt once the day's spend reaches a threshold. The idle check fails open (unavailable snapshot treated as not idle), the ledger sum ignores malformed lines and missing files, and the cap comparison uses >= so an exact match triggers. The first cycle of a UTC day is never skipped; the kill switch IDLE_SKIP_ENABLED is read at call time.

## Related

- part of [[auto-loop-core-engine]] — Idle detection and discretionary cap logic live in auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
