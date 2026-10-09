---
name: Production Mechanism Guard
slug: production-mechanism-guard
type: file
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 82fd9dfa80c4f0c916c506e6a44db71dbfd6ee1c0421bcedf8d255b77c3bfd7e
sources_digest: 263f9d310def4297100620a3e13cbafec2875dee071601a272efb7f353727c6b
links:
  - to: auto-loop-harness
    relation: validates
    description: >-
      --check-sync verifies CLAUDE.md rule coverage; guards writes to
      auto-loop.sh
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

A PreToolUse tripwire hook for Claude Code that mechanically blocks unplanned writes to protected production surfaces (scripts/core/auto-loop.sh, dashboard/server.py, Dockerfile, runtime.env) unless a fresh 120-minute marker file exists. Includes a --check-sync drift detector that parses CLAUDE.md's rule section and verifies every backtick-referenced surface is covered. Deliberately fail-open on malformed stdin so harness format changes don't lock all edits, and no-ops when CLAUDE_PROJECT_DIR points to /app (deferring to PROMPT.md's OPREQ authorization machine). Philosophy is a tripwire, not a boundary — sed -i in Bash bypasses it entirely.

## Related

- validates [[auto-loop-harness]] — --check-sync verifies CLAUDE.md rule coverage; guards writes to auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
