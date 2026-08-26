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
  - to: auto-loop-core
    relation: validates
    description: >-
      The guard protects auto-loop.sh and other production surfaces from
      unapproved edits; --check-sync validates the documented rule matches the
      guard.
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

A PreToolUse hook (scripts/prod-mechanism-guard.py) that blocks edits to protected production surfaces unless a time-limited approval marker exists, plus its regression suite. It fails open on malformed stdin or inside the container, treats itself as a tripwire, and has a --check-sync mode that detects drift between CLAUDE.md's documented protected list and the actual PROTECTED_* lists.

## Related

- validates [[auto-loop-core]] — The guard protects auto-loop.sh and other production surfaces from unapproved edits; --check-sync validates the documented rule matches the guard.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
