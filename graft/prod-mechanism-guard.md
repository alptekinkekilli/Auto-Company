---
name: prod mechanism guard
slug: prod-mechanism-guard
type: file
sources:
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
sources_digest: bdb259f08d24f80a2819e8b7ef84bd6ad99c9a2524f41664136ac3d5c33790b4
links:
  - to: auto-loop-core-engine
    relation: validates
    description: auto-loop.sh is a protected production surface blocked by the guard
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

prod-mechanism-guard.py is a PreToolUse hook blocking edits to production-critical surfaces (auto-loop.sh, send-gate.py, deploy/runtime.env). A fresh .claude/.prod-change-approved marker grants a 3-hour override window (stale markers rejected via os.utime). Fail-open on malformed JSON, no-op for container paths like /app, non-Edit tools untouched. --check-sync parses the ## Prod-Mechanism Change Rule section of CLAUDE.md to detect drift between documented and actual PROTECTED_* lists.

## Related

- validates [[auto-loop-core-engine]] — auto-loop.sh is a protected production surface blocked by the guard
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
