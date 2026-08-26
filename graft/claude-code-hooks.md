---
name: Claude Code hooks
slug: claude-code-hooks
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: df90f44c6e799ee5505f180b9c47889d0ebfe295a0fd99b661438f51a8dd6bf2
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
sources_digest: cca34ac3b6513cc92ece2da41fd8889b0a8a7733795a80bf4d24d702af1f4555
links:
  - to: auto-loop-core
    relation: configures
    description: >-
      prod-mechanism-guard protects scripts/core/auto-loop.sh,
      dashboard/server.py, Dockerfile, deploy/runtime.env.
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

The SessionStart/PreToolUse hooks that shape the agent's context and guard its edits. session-brief.py injects measured git state (never blocking, never writing secrets, measurements override summary text). prod-mechanism-guard.py blocks edits to protected production surfaces unless a time-limited approval marker exists, fails open on malformed stdin or inside a container, and --check-sync enforces the protected list matches CLAUDE.md.

## Related

- configures [[auto-loop-core]] — prod-mechanism-guard protects scripts/core/auto-loop.sh, dashboard/server.py, Dockerfile, deploy/runtime.env.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
