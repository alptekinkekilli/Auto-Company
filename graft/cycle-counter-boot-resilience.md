---
name: Cycle counter & boot resilience
slug: cycle-counter-boot-resilience
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
sources_digest: e194de420548d25b6b0526952beef3afd4e09cf45409d738794c398f9075d5af
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The counter logic lives in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The cycle-counter seed/persist logic in auto-loop.sh that keeps the counter monotonic across redeploys (persisted file wins, self-heals to highest cycle-NNNN log, corrupt counter falls back to 0) and the fail-open/fail-closed conventions around it. Tests run the real seed block under the same set -euo pipefail options as production to catch crash-loop bugs.

## Related

- part of [[auto-loop-core-engine]] — The counter logic lives in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
