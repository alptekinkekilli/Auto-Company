---
name: prod mechanism guard
slug: prod-mechanism-guard
type: system
sources:
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: 35954dc42d5b690d0b8fe77e00f7b4d6ae3bb8b635aa4b6914085968db398d73
links:
  - to: rfq-operations
    relation: validates
    description: rfq-send.py must be registered in the guard and pass --check-sync
  - to: send-gate
    relation: validates
    description: >-
      send-gate.py is a protected surface; rfq-send.py must be registered in the
      guard
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

prod-mechanism-guard.py is a PreToolUse hook blocking edits to production-critical surfaces (scripts/core/auto-loop.sh, scripts/ops/send-gate.py, deploy/runtime.env, etc.) with exit code 2, granting a 3-hour override via a fresh .claude/.prod-change-approved marker (stale markers rejected via os.utime). It fails open on malformed JSON, no-ops on container paths like /app, and leaves non-Edit tools untouched. --check-sync parses the ## Prod-Mechanism Change Rule section of CLAUDE.md to detect drift between documented protected surfaces and the actual PROTECTED_* list, failing closed on missing sections.

## Related

- validates [[rfq-operations]] — rfq-send.py must be registered in the guard and pass --check-sync
- validates [[send-gate]] — send-gate.py is a protected surface; rfq-send.py must be registered in the guard
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
