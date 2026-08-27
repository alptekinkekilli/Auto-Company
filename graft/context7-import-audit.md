---
name: Context7 import audit
slug: context7-import-audit
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
sources_digest: f7ae9d084de3310f18d8d2a904d56dc005125358dc07afc4d0c220fae1cedc7a
links:
  - to: auto-loop-core-engine
    relation: uses
generator:
  version: 1
covers:
  - symbol: externals
    kind: function
    at: 'scripts/ops/context7-check.py:L59-L75'
  - symbol: scan
    kind: function
    at: 'scripts/ops/context7-check.py:L78-L108'
  - symbol: walk_calls
    kind: function
    at: 'scripts/ops/context7-check.py:L111-L122'
  - symbol: verdict
    kind: function
    at: 'scripts/ops/context7-check.py:L125-L138'
  - symbol: main
    kind: function
    at: 'scripts/ops/context7-check.py:L141-L170'
---
<!-- context:generated:start -->
## Summary

context7-check.py audits cycles to ensure external library imports are accompanied by a Context7 documentation lookup; must not fire on the project's own stdlib-only ops scripts to avoid false alarms.

## Related

- uses [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
