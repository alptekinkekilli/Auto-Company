---
name: tool-usage audit engine
slug: tool-usage-audit-engine
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
sources_digest: 64269fae6aa64ebe38255ded448bb71bc6bb83445d9866ecf43b9dddb18f813a
links:
  - to: tool-usage-audit-regression-suite
    relation: validates
    description: >-
      The test suite asserts categorization, ledger idempotence, and reporting
      behavior.
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

Categorizes tool usage from a jcode NDJSON event stream, combining script + MCP tools (airtable_r/w, browser harness + MCP), recording per-MCP-tool-name counts only for MCP tools (not bash), and maintaining a ledger keyed by cycle with idempotent re-auditing. Supports --app, --names, and --report flags; --report exits 0 even when the ndjson directory is missing. Counts browse-extract.py harness as browser usage to prevent faking A/B drops.

## Related

- validates [[tool-usage-audit-regression-suite]] — The test suite asserts categorization, ledger idempotence, and reporting behavior.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
