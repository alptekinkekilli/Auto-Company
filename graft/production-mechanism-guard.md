---
name: Production mechanism guard
slug: production-mechanism-guard
type: file
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
sources_digest: a8778c76c2d84b2d7e9fe72981362b4bad9b3fde2625b2005cf87674c41bea8c
links:
  - to: auto-loop-orchestration-core
    relation: validates
generator:
  version: 1
covers:
  - symbol: is_protected
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L49-L52'
  - symbol: check_sync
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L55-L81'
  - symbol: main
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L84-L126'
---
<!-- context:generated:start -->
## Summary

A PreToolUse tripwire hook that blocks unplanned writes to protected production surfaces (auto-loop.sh, dashboard/server.py, Dockerfile, runtime.env) unless a fresh .prod-change-approved marker exists. Fail-open on malformed stdin; no-ops when CLAUDE_PROJECT_DIR is /app.

## Related

- validates [[auto-loop-orchestration-core]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
