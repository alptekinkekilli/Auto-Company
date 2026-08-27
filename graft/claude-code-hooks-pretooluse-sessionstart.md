---
name: Claude Code hooks (PreToolUse/SessionStart)
slug: claude-code-hooks-pretooluse-sessionstart
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: df90f44c6e799ee5505f180b9c47889d0ebfe295a0fd99b661438f51a8dd6bf2
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
sources_digest: 569be6755fcfc4da6381cf4afc5e059f8838053811c1b1d328a5f480dbd7665a
links:
  - to: auto-loop-core
    relation: configures
    description: >-
      prod-mechanism-guard protects scripts/core/auto-loop.sh and
      dashboard/server.py from unapproved edits; session-brief feeds context
      into each session.
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

Two hook scripts that enforce policy at the harness boundary. prod-mechanism-guard.py is a PreToolUse hook blocking edits to protected production surfaces unless a time-limited approval marker exists, and fails open inside the container to avoid locking out autonomous cycles. session-brief.py is a SessionStart hook injecting a measured, real-time git/state brief, preferring measured facts over claims and never blocking the session.

## Related

- configures [[auto-loop-core]] — prod-mechanism-guard protects scripts/core/auto-loop.sh and dashboard/server.py from unapproved edits; session-brief feeds context into each session.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
