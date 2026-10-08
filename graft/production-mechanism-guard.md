---
name: Production Mechanism Guard
slug: production-mechanism-guard
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 9f5bbd179e642477f15485da93a5390b583697954e54da99cd4e2af00dce5eb8
sources_digest: 3f4ade02ffd2d2890146fa5ad4aa23f82339e729967973b9fe6d5670591736d3
links:
  - to: auto-loop-harness
    relation: validates
    description: >-
      Blocks unplanned edits to auto-loop.sh and other protected surfaces;
      --check-sync is invoked by tests to verify rule coverage.
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

A PreToolUse tripwire hook for Claude Code that mechanically blocks unplanned writes to protected production surfaces (scripts/core/auto-loop.sh, dashboard/server.py, Dockerfile, runtime.env) unless a fresh .claude/.prod-change-approved marker (120-min TTL) exists. It is deliberately fail-open on malformed stdin so harness format changes don't lock all edits, and no-ops entirely when CLAUDE_PROJECT_DIR points to /app, deferring to PROMPT.md's OPREQ authorization machine for autonomous cycles. A --check-sync drift detector parses CLAUDE.md's rule section and verifies every backtick-referenced surface is covered. Known limitation: sed -i in Bash bypasses the guard entirely — it is a tripwire, not a boundary.

## Related

- validates [[auto-loop-harness]] — Blocks unplanned edits to auto-loop.sh and other protected surfaces; --check-sync is invoked by tests to verify rule coverage.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
