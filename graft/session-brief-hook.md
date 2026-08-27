---
name: Session brief hook
slug: session-brief-hook
type: system
sources:
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
sources_digest: 77a08c55273fd8415d52a44771613fd9b92c20dead94083ce126b831c87145a6
links:
  - to: compact-ritual
    relation: uses
    description: Checks /tmp/compact-preflight.md for open items from a prior compact.
generator:
  version: 1
covers:
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L19-L23'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L26-L63'
---
<!-- context:generated:start -->
## Summary

SessionStart hook that injects a measured git-state brief, never blocking the session, never writing secrets, and preferring measured facts over claims. Optionally runs .claude/brief-extra.sh and surfaces fresh compact preflight items.

## Related

- uses [[compact-ritual]] — Checks /tmp/compact-preflight.md for open items from a prior compact.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
