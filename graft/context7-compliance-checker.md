---
name: Context7 compliance checker
slug: context7-compliance-checker
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
sources_digest: 7b9324b6606ae2451e7e0e246f5f0afc951e0c21403a03d682250a5b8758309e
links:
  - to: auto-company-loop-core
    relation: validates
    description: Judges whether cycles violated the Context7-first rule.
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

Compliance checker that inspects per-cycle ndjson logs to detect whether an agent wrote code importing an external library without first calling the Context7 MCP tool. Deliberately avoids prefiltering on exact JSON strings (which previously caused silent false negatives), parses JSON lines rather than regexing code payloads, and reports to the LOG rather than blocking or pushing to Telegram.

## Related

- validates [[auto-company-loop-core]] — Judges whether cycles violated the Context7-first rule.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
