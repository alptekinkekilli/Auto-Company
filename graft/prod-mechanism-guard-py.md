---
name: prod-mechanism-guard.py
slug: prod-mechanism-guard-py
type: file
sources:
  - path: scripts/prod-mechanism-guard.py
    hash: e3d5c01038affa27aaed85106b6b8ff0705c6be14fa3b2caa1c21144fde5acee
sources_digest: a8778c76c2d84b2d7e9fe72981362b4bad9b3fde2625b2005cf87674c41bea8c
links:
  - to: auto-loop-sh-core-loop
    relation: validates
  - to: send-gate-py
    relation: validates
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

PreToolUse hook blocking edits to production-critical surfaces (auto-loop.sh, send-gate.py, runtime.env) with a 3-hour override marker; also --check-sync parses CLAUDE.md's Prod-Mechanism Change Rule to detect drift between documented and actual protected lists. Fail-open on malformed JSON.

## Related

- validates [[auto-loop-sh-core-loop]]
- validates [[send-gate-py]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
