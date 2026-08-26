---
name: session-brief-hook
slug: session-brief-hook
type: system
sources:
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
sources_digest: 77a08c55273fd8415d52a44771613fd9b92c20dead94083ce126b831c87145a6
links:
  - to: auto-loop-core
    relation: configures
    description: >-
      Injects measured state into the session context that the loop's prompts
      build on.
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

A SessionStart hook (scripts/session-brief.py) that injects a measured real-time git/session brief into context, replacing stale hand-written resume text. It never blocks the session, never writes secrets, and always prefers measured facts over claims, optionally running a project brief-extra.sh and surfacing fresh compact-preflight items.

## Related

- configures [[auto-loop-core]] — Injects measured state into the session context that the loop's prompts build on.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
