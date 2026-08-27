---
name: Prod-mechanism guard & session brief
slug: prod-mechanism-guard-session-brief
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: df90f44c6e799ee5505f180b9c47889d0ebfe295a0fd99b661438f51a8dd6bf2
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
sources_digest: 569be6755fcfc4da6381cf4afc5e059f8838053811c1b1d328a5f480dbd7665a
links:
  - to: auto-loop-core-auto-loop-sh
    relation: validates
    description: >-
      Guard protects auto-loop.sh, dashboard/server.py, Dockerfile from
      unapproved edits.
generator:
  version: 1
covers:
  - symbol: is_protected
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L48-L51'
  - symbol: check_sync
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L54-L80'
  - symbol: main
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L83-L125'
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L19-L23'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L26-L63'
---
<!-- context:generated:start -->
## Summary

PreToolUse hook (prod-mechanism-guard.py) blocks edits to protected production surfaces unless a time-limited approval marker exists, failing open in container. SessionStart hook (session-brief.py) injects measured git state, never blocking, never writing secrets.

## Related

- validates [[auto-loop-core-auto-loop-sh]] — Guard protects auto-loop.sh, dashboard/server.py, Dockerfile from unapproved edits.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
