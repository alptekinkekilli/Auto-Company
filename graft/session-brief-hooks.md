---
name: session brief & hooks
slug: session-brief-hooks
type: system
sources:
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
sources_digest: 77a08c55273fd8415d52a44771613fd9b92c20dead94083ce126b831c87145a6
links: []
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

SessionStart hook (session-brief.py) that injects a measured git-state brief, preferring measured facts over claims, never blocking the session, and never writing secrets.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
