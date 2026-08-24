---
name: Tool usage audit
slug: tool-usage-audit
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
sources_digest: a34a96243cdbd57c7896fc7d5f5a4dde3fcdd8a6a1bca52ea9921948d1a6dab2
links:
  - to: mcp-config-key-handling
    relation: uses
    description: per-MCP-tool-name counts only for MCP tools
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

Audits jcode NDJSON event streams, categorizing tool usage (script+MCP combined), maintaining an idempotent ledger, and re-auditing rewritten cycle files (cycle counter resets on container restart) rather than deduping by filename. Counts browse-extract harness as browser usage to prevent faking A/B drops.

## Related

- uses [[mcp-config-key-handling]] — per-MCP-tool-name counts only for MCP tools
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
