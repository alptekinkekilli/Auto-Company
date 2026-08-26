---
name: tool-usage audit regression suite
slug: tool-usage-audit-regression-suite
type: system
sources:
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
sources_digest: cba460eef4963bdc24ab59d1ddd5c9e0777b7c6fa78ddf2ea20f94c8ce1e9ab6
links:
  - to: tool-usage-audit-engine
    relation: validates
    description: >-
      Asserts categorization, idempotence, and reporting behavior of the audit
      script.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash test suite for tool-usage-audit.py. Generates a synthetic jcode NDJSON stream with deliberately fragmented tool_input deltas split mid-token, and asserts categorization, ledger idempotence (second run appends nothing), backfilling of new cycle-0002.ndjson, re-auditing of a rewritten cycle-0001.ndjson (cycle counter resets on container restart, so dedup must be by content not filename), and that --names reports the ledger without mutating it.

## Related

- validates [[tool-usage-audit-engine]] — Asserts categorization, idempotence, and reporting behavior of the audit script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
