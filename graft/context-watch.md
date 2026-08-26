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
    description: Emits compact-ritual directive that triggers the compact preflight hook.
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

Claude Code hook monitoring context-window fullness. Reads transcript usage field, sums input/cache_read/cache_creation tokens, computes % against auto-escalating window (200k up to 2M). Warns at 50%, emits compact-ritual directive at 60% via hookSpecificOutput.additionalContext (must be nested there or silently ignored). Per-session state in /tmp so each threshold fires once; drop below 40% re-arms. Fail-open.

## Related

- uses [[compact-preflight]] — Emits compact-ritual directive that triggers the compact preflight hook.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
