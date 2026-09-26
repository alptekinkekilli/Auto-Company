---
name: Prod-mechanism guard
slug: prod-mechanism-guard
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
sources_digest: 85f0fc7428c6e4e3dfe8a3574ea24ed99ff361f071029bc7d1a9cbef79456bc1
links:
  - to: auto-loop-harness
    relation: validates
    description: Protects the loop's own surfaces from unplanned edits.
  - to: send-gate
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

A PreToolUse tripwire hook that mechanically blocks unplanned writes to protected production surfaces (auto-loop.sh, dashboard/server.py, Dockerfile, runtime.env) unless a fresh .prod-change-approved marker exists. Fail-open on malformed stdin so harness format changes don't lock all edits; no-ops entirely when CLAUDE_PROJECT_DIR points to /app, deferring to PROMPT.md's OPREQ authorization machine. A tripwire, not a boundary — sed -i in Bash bypasses it.

## Related

- validates [[auto-loop-harness]] — Protects the loop's own surfaces from unplanned edits.
- validates [[send-gate]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
