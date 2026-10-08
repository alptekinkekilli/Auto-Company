---
name: cycle counter persistence
slug: cycle-counter-persistence
type: concept
sources:
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
sources_digest: d21fe4ccd33e13c7c9b5188ed04aa2d284d3b759dab87c80f8c857ebe08ceff3
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The counter logic lives in auto-loop.sh's seed block and persist line
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The cycle counter must be monotonic across container redeploys, never silently resetting to 1. It is seeded from a persisted counter file, self-heals to the highest cycle-NNNN log on disk when the file is missing, strips non-digits from corrupt values, and persists after each cycle. The seed block and persist line are extracted verbatim by tests and run under the same set -euo pipefail as production, since omitting those options would mask a crash-loop bug.

## Related

- part of [[auto-loop-core-engine]] — The counter logic lives in auto-loop.sh's seed block and persist line
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
