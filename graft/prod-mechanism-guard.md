---
name: Prod-mechanism guard
slug: prod-mechanism-guard
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: df90f44c6e799ee5505f180b9c47889d0ebfe295a0fd99b661438f51a8dd6bf2
sources_digest: 3b577b3d1f7a1d17923d334bebe6766de49a839fbd51de39aee05bf1572b4657
links:
  - to: auto-loop-core-engine
    relation: validates
    description: Blocks edits to auto-loop.sh and other protected surfaces.
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

PreToolUse hook (prod-mechanism-guard.py) that blocks edits to protected production surfaces unless a time-limited approval marker exists. Fails open inside the container to avoid locking out autonomous cycles, and --check-sync enforces the protected list matches CLAUDE.md.

## Related

- validates [[auto-loop-core-engine]] — Blocks edits to auto-loop.sh and other protected surfaces.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
