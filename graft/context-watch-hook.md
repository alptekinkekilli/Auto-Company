---
name: Context Watch Hook
slug: context-watch-hook
type: file
sources:
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: e120476879431ac8f01406f0c7056c596e84ad05a3bdffa80c27718e3d312c80
links: []
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

Claude Code hook that monitors context-window fullness, summing input/cache tokens from the last assistant message in the transcript. Emits a warning at 50% and a compact-ritual directive at 60%, with per-session state so each threshold fires once and re-arms below 40% after compaction. Fail-open (returns 0 on any error); the additional context must be nested inside hookSpecificOutput or it is silently ignored.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
