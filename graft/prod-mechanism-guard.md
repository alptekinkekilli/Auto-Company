---
name: prod-mechanism guard
slug: prod-mechanism-guard
type: file
sources:
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: 35954dc42d5b690d0b8fe77e00f7b4d6ae3bb8b635aa4b6914085968db398d73
links:
  - to: send-gate-outreach-policy
    relation: validates
    description: rfq-send.py must be registered in the guard and pass --check-sync
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/prod-mechanism-guard.py is a PreToolUse hook blocking edits to production-critical surfaces (auto-loop.sh, send-gate.py, deploy/runtime.env) with a 3-hour override window via a .claude/.prod-change-approved marker (stale markers rejected via os.utime). It fails open on malformed JSON, no-ops on container paths like /app, and --check-sync parses the '## Prod-Mechanism Change Rule' section of CLAUDE.md to detect drift between documented and actual PROTECTED_* lists, failing closed on missing sections.

## Related

- validates [[send-gate-outreach-policy]] — rfq-send.py must be registered in the guard and pass --check-sync
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
