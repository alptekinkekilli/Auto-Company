---
name: Production surface protection
slug: production-surface-protection
type: system
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 82fd9dfa80c4f0c916c506e6a44db71dbfd6ee1c0421bcedf8d255b77c3bfd7e
sources_digest: 263f9d310def4297100620a3e13cbafec2875dee071601a272efb7f353727c6b
links:
  - to: auto-loop-harness-budget-governance
    relation: validates
    description: >-
      The --check-sync drift detector verifies auto-loop.sh and other protected
      surfaces are covered by the rule.
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

prod-mechanism-guard.py is a PreToolUse tripwire hook that blocks unplanned writes to protected production surfaces (scripts/core/auto-loop.sh, dashboard/server.py, Dockerfile, runtime.env) unless a fresh 120-minute marker exists. Includes a --check-sync drift detector verifying every backtick-referenced surface in CLAUDE.md is covered. Deliberately fail-open on malformed stdin so harness format changes don't lock all edits, and no-ops when CLAUDE_PROJECT_DIR points to /app (deferring to PROMPT.md's OPREQ authorization machine). Design philosophy is a tripwire, not a boundary — catches unplanned diving, not malicious intent; sed -i in Bash bypasses it entirely.

## Related

- validates [[auto-loop-harness-budget-governance]] — The --check-sync drift detector verifies auto-loop.sh and other protected surfaces are covered by the rule.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
