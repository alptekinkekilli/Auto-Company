---
name: Context Watch Hook
slug: context-watch-hook
type: file
sources:
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: e120476879431ac8f01406f0c7056c596e84ad05a3bdffa80c27718e3d312c80
links:
  - to: compact-ritual-tooling
    relation: uses
    description: >-
      Emits the compact-ritual directive that triggers the
      preflight/lint/postcheck hooks
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

A Claude Code hook that monitors context-window fullness during a session, reading the transcript's usage field and summing input/cache tokens. Emits a warning at 50% and a compact-ritual directive at 60% via hookSpecificOutput.additionalContext (which must be nested there or it is silently ignored). State persisted per session in /tmp so each threshold fires once per session, re-armed when usage drops below 40% after compaction. Window size auto-escalates through tiers up to 2M because the first live run measured 257% against the default 200k.

## Related

- uses [[compact-ritual-tooling]] — Emits the compact-ritual directive that triggers the preflight/lint/postcheck hooks
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
