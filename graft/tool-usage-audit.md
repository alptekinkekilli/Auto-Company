---
name: Tool usage audit
slug: tool-usage-audit
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 1e21a81523cfbf8e4c6b9b1ee7782201c293b73feebe7494fd91494587ec9a4e
  - path: tests/test_tool_usage_audit.sh
    hash: 827e85f8e8e61beb4d2796204a7343d06479be42ced46e66c27c8582f231f2f2
sources_digest: b3b9d5c24bf05318b94685ee08ba679a33aedafaad76d0019101014c37f37e4e
links:
  - to: web-research-cost-model
    relation: uses
    description: Both analyze jcode NDJSON event streams from logs/cycle-ndjson/.
generator:
  version: 1
covers:
  - symbol: calls_from_ndjson
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L43-L65'
  - symbol: categorize
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L68-L114'
  - symbol: main
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L117-L244'
  - symbol: dump
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L170-L183'
---
<!-- context:generated:start -->
## Summary

tool-usage-audit.py categorizes tool usage from jcode event streams (tool_start, fragmented tool_input deltas, tool_exec) into a durable NDJSON ledger. Reassembles split JSON fragments, dedups by mtime (not filename, since cycle numbers reset on container restart), and records per-MCP-tool counts only for MCP tools to keep the ledger lean.

## Related

- uses [[web-research-cost-model]] — Both analyze jcode NDJSON event streams from logs/cycle-ndjson/.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
