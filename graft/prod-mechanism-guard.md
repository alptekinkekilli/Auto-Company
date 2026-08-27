---
name: prod-mechanism-guard
slug: prod-mechanism-guard
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: df90f44c6e799ee5505f180b9c47889d0ebfe295a0fd99b661438f51a8dd6bf2
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
sources_digest: 85f695b540190c148b455d6cc63e72dbb881bcb53a6cf3d680c51a434fc47b16
links:
  - to: auto-loop
    relation: validates
    description: >-
      Guard blocks edits to scripts/core/auto-loop.sh unless an override marker
      is fresh.
  - to: send-gate
    relation: validates
    description: Guard blocks edits to scripts/ops/send-gate.py.
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
---
<!-- context:generated:start -->
## Summary

PreToolUse hook that blocks edits to production-critical surfaces (scripts/core/auto-loop.sh, scripts/ops/send-gate.py, deploy/runtime.env) with a 3-hour override window granted by a fresh .claude/.prod-change-approved marker; fails open on malformed JSON and ignores container paths like /app. A --check-sync mode parses the '## Prod-Mechanism Change Rule' section of CLAUDE.md to detect drift between documented protected surfaces and the actual PROTECTED_* list, failing closed on missing sections.

## Related

- validates [[auto-loop]] — Guard blocks edits to scripts/core/auto-loop.sh unless an override marker is fresh.
- validates [[send-gate]] — Guard blocks edits to scripts/ops/send-gate.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
