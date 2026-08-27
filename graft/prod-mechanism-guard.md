---
name: prod_mechanism_guard
slug: prod-mechanism-guard
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: f3048e0e552e08587e98750fa82cfc6aaf3415016df85a47fd6ab4b79c70696f
links:
  - to: operator-request-notify
    relation: validates
    description: The notify script is a protected production surface.
  - to: send-gate
    relation: validates
    description: rfq-send.py must be registered in the guard and pass --check-sync.
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

A PreToolUse hook (scripts/prod-mechanism-guard.py) that blocks edits to production-critical surfaces (auto-loop.sh, send-gate.py, deploy/runtime.env, and others) with exit code 2, unless a fresh .claude/.prod-change-approved marker grants a 3-hour override window. It fails open on malformed JSON, no-ops on container paths like /app, and ignores non-Edit tools. A --check-sync mode parses the '## Prod-Mechanism Change Rule' section of CLAUDE.md to detect drift between documented protected surfaces and the actual PROTECTED_* list, failing closed on missing sections.

## Related

- validates [[operator-request-notify]] — The notify script is a protected production surface.
- validates [[send-gate]] — rfq-send.py must be registered in the guard and pass --check-sync.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
