---
name: tool usage audit
slug: tool-usage-audit
type: file
sources:
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
sources_digest: cba460eef4963bdc24ab59d1ddd5c9e0777b7c6fa78ddf2ea20f94c8ce1e9ab6
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

tool-usage-audit.py categorizes jcode NDJSON event streams, handling fragmented tool_input deltas split mid-token, combining script+MCP tool counts (airtable_r/airtable_w, browser harness+MCP), idempotent ledger (second run appends nothing), re-audits rewritten cycle files rather than deduping by filename, --names reports without mutating, --report exits 0 even when ndjson dir missing. Counts browse-extract.py harness as browser usage to prevent faking A/B drops.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
