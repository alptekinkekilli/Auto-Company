---
name: Context Watch
slug: context-watch
type: file
sources:
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: e120476879431ac8f01406f0c7056c596e84ad05a3bdffa80c27718e3d312c80
links:
  - to: compact-preflight
    relation: uses
    description: >-
      The compact-ritual directive at 60% triggers the compact flow that
      compact-preflight.py measures.
generator:
  version: 1
covers:
  - symbol: kullanim
    kind: function
    at: 'scripts/context-watch.py:L33-L50'
  - symbol: main
    kind: function
    at: 'scripts/context-watch.py:L53-L102'
---
<!-- context:generated:start -->
## Summary

Claude Code hook monitoring context-window fullness during a session. Reads the session transcript, sums input/cache_read/cache_creation tokens, emits a warning at 50% or a compact-ritual directive at 60% via hookSpecificOutput.additionalContext. State persisted per session in /tmp/context-watch-<sid>.json so each threshold fires only once per session; drop below 40% after compaction re-arms thresholds. Fail-open (returns 0 on any error). Gotcha: additional context must be nested inside hookSpecificOutput or silently ignored; window size not assumed fixed because first live run measured 257% against default.

## Related

- uses [[compact-preflight]] — The compact-ritual directive at 60% triggers the compact flow that compact-preflight.py measures.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
