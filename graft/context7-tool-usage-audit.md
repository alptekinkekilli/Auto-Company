---
name: Context7 & tool-usage audit
slug: context7-tool-usage-audit
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
sources_digest: cc53b12c50ac90d87af77f15e693fdcdd8514f00b68d83326c9571070c2e195f
links:
  - to: ops-probe-audit-scripts
    relation: part_of
    description: >-
      tool-usage-audit is one of the probe family; context7-check is a cycle
      auditor.
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
  - symbol: calls_from_ndjson
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L43-L65'
  - symbol: categorize
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L68-L121'
  - symbol: main
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L124-L251'
  - symbol: dump
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L177-L190'
---
<!-- context:generated:start -->
## Summary

context7-check.py audits cycles to ensure external library imports are accompanied by a Context7 documentation lookup, and must not fire on the project's own stdlib-only ops scripts. tool-usage-audit.py maintains the durable per-cycle tool ledger with honest browser vs browser_mcp denominators for the harness A/B test.

## Related

- part of [[ops-probe-audit-scripts]] — tool-usage-audit is one of the probe family; context7-check is a cycle auditor.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
