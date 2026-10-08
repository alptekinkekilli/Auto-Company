---
name: Prod-Mechanism Guard
slug: prod-mechanism-guard
type: file
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 82fd9dfa80c4f0c916c506e6a44db71dbfd6ee1c0421bcedf8d255b77c3bfd7e
  - path: tests/test_prod_mechanism_guard.sh
    hash: 1c8df67eca679e21cbbe4ea2daac7f761fc952f17b25f99d2673a4782ffa6824
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: e40c0d8a9ab7165c0f6f190dfe88130c8a12d9f88cff965a0eec2c8e12ad0906
links:
  - to: auto-loop-harness
    relation: validates
    description: >-
      Blocks unplanned edits to auto-loop.sh and other protected surfaces;
      --check-sync verifies CLAUDE.md rule coverage.
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

prod-mechanism-guard.py is a PreToolUse hook blocking edits to production-critical surfaces (scripts/core/auto-loop.sh, scripts/ops/send-gate.py, deploy/runtime.env, etc.) with exit code 2, granting a 3-hour override via a fresh .claude/.prod-change-approved marker (stale markers rejected via os.utime). It fails open on malformed JSON, no-ops on container paths like /app, and leaves non-Edit tools untouched. --check-sync parses the ## Prod-Mechanism Change Rule section of CLAUDE.md to detect drift between documented protected surfaces and the actual PROTECTED_* list, failing closed on missing sections.

## Related

- validates [[auto-loop-harness]] — Blocks unplanned edits to auto-loop.sh and other protected surfaces; --check-sync verifies CLAUDE.md rule coverage.
- validates [[rfq-operations]] — rfq-send.py must be registered in the guard and pass --check-sync
- validates [[send-gate]] — send-gate.py is a protected surface; rfq-send.py must be registered in the guard
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
