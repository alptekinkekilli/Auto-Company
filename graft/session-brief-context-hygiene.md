---
name: Session brief & context hygiene
slug: session-brief-context-hygiene
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
sources_digest: a497ac0ec6c08c8ffe81aa532cb214d58e4367ce87d8d7c06792e89f33cac2fb
links:
  - to: auto-loop-core-engine
    relation: uses
    description: The brief and context checks feed the loop's context.
generator:
  version: 1
covers:
  - symbol: externals
    kind: function
    at: 'scripts/ops/context7-check.py:L59-L75'
  - symbol: scan
    kind: function
    at: 'scripts/ops/context7-check.py:L78-L108'
  - symbol: walk_calls
    kind: function
    at: 'scripts/ops/context7-check.py:L111-L122'
  - symbol: verdict
    kind: function
    at: 'scripts/ops/context7-check.py:L125-L138'
  - symbol: main
    kind: function
    at: 'scripts/ops/context7-check.py:L141-L170'
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L19-L23'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L26-L63'
---
<!-- context:generated:start -->
## Summary

session-brief.py is a SessionStart hook that injects a measured real-time brief (git state, optional .claude/brief-extra.sh, compact preflight) replacing stale hand-written resume text; never blocks, never writes secrets, and states that measurements override summary text. The context7-check.py audit ensures external imports are accompanied by a Context7 lookup, deliberately silent for the project's own stdlib-only ops scripts.

## Related

- uses [[auto-loop-core-engine]] — The brief and context checks feed the loop's context.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
