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

scripts/ops/tool-usage-audit.py categorizes a jcode NDJSON event stream (handling fragmented tool_input deltas split mid-token), with ledger idempotence, backfilling new cycle files, and re-auditing rewritten cycle files (cycle counter resets on container restart) rather than deduping by filename. It counts the browse-extract.py harness as browser usage to prevent faking A/B drops, and --report exits 0 even when the ndjson dir is missing.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
