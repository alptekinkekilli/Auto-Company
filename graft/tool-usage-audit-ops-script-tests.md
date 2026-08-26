---
name: tool-usage-audit ops script + tests
slug: tool-usage-audit-ops-script-tests
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
sources_digest: a34a96243cdbd57c7896fc7d5f5a4dde3fcdd8a6a1bca52ea9921948d1a6dab2
links: []
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
---
<!-- context:generated:start -->
## Summary

scripts/ops/tool-usage-audit.py and its bash suite tests/test_tool_usage_audit.sh. Audits a jcode NDJSON event stream, categorizing tool usage (ctx7, airtable_r/w, linear, browser harness+MCP, browser_mcp, graft), with per-MCP-tool-name counts recorded only for MCP tools. Key invariants tested: ledger idempotence (second run appends nothing), backfilling new cycle files, re-auditing a rewritten cycle file whose counter resets on container restart (not deduped by filename), --names reports without mutating, --report exits 0 on missing ndjson dir, and browse-extract.py harness counts as browser usage to prevent faking A/B drops. Handles tool_input deltas split mid-token.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
