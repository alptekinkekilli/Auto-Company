---
name: ops_audit_tools
slug: ops-audit-tools
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: 83cd30a8031b08f9e1839622d27786cdce5a893cac0719b399c733a2a7945984
links:
  - to: auto-loop
    relation: validates
    description: >-
      Audits the event streams and daily logs produced by the loop's engine
      cycles.
generator:
  version: 1
covers:
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
  - symbol: ts_of
    kind: function
    at: 'scripts/ops/turn-audit.py:L74-L78'
  - symbol: scan
    kind: function
    at: 'scripts/ops/turn-audit.py:L81-L112'
  - symbol: floor_usd
    kind: function
    at: 'scripts/ops/turn-audit.py:L115-L118'
  - symbol: summary_line
    kind: function
    at: 'scripts/ops/turn-audit.py:L121-L139'
  - symbol: main
    kind: function
    at: 'scripts/ops/turn-audit.py:L142-L155'
---
<!-- context:generated:start -->
## Summary

scripts/ops audit tools that turn synthetic or real event streams into ledgers and reports. tool-usage-audit.py categorizes jcode NDJSON events (fragmented tool_input deltas, MCP vs script vs harness counts), is idempotent, backfills new cycle files, re-audits rewritten cycle files (cycle counter resets on container restart) rather than deduping by filename, and counts browse-extract.py as browser usage to prevent faking A/B drops. turn-audit.py implements the turn-economy policy (section 4) with verdict thresholds (CHATTY/BLOATED/ok) and --summary-last.

## Related

- validates [[auto-loop]] — Audits the event streams and daily logs produced by the loop's engine cycles.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
