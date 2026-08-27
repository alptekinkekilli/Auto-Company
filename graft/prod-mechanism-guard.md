---
name: prod_mechanism_guard
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
      Protects auto-loop.sh from unapproved edits; the guard's PROTECTED_* list
      must stay in sync with CLAUDE.md.
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

A PreToolUse hook (scripts/prod-mechanism-guard.py) that blocks edits to production-critical surfaces (scripts/core/auto-loop.sh, scripts/ops/send-gate.py, deploy/runtime.env) with exit code 2, granting a 3-hour override via a fresh .claude/.prod-change-approved marker (stale markers rejected via os.utime). Fails open on malformed JSON, no-ops on container paths like /app, and leaves non-Edit tools untouched. --check-sync parses the '## Prod-Mechanism Change Rule' section of CLAUDE.md to detect drift between documented protected surfaces and the actual PROTECTED_* list, failing closed on missing sections.

## Related

- validates [[auto-loop]] — Protects auto-loop.sh from unapproved edits; the guard's PROTECTED_* list must stay in sync with CLAUDE.md.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
