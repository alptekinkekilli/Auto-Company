---
name: Airtable read wrapper
slug: airtable-read-wrapper
type: system
sources:
  - path: scripts/ops/airtable-read.py
    hash: 148f66145510c90e03256b7b37853122bcd892d51cba67f095ce700a0895e3e2
sources_digest: 033e10c880871ae2700842eb1538da1575c96b66efb3906e79a6cb62959dd4bf
links:
  - to: airtable-ops-watchers
    relation: uses
    description: Watchers paginate records through this wrapper's scoping conventions.
generator:
  version: 1
covers:
  - symbol: Refusal
    kind: class
    at: 'scripts/ops/airtable-read.py:L68-L69'
  - symbol: load_env
    kind: function
    at: 'scripts/ops/airtable-read.py:L72-L92'
  - symbol: load_keychain
    kind: function
    at: 'scripts/ops/airtable-read.py:L95-L111'
  - symbol: build_params
    kind: function
    at: 'scripts/ops/airtable-read.py:L114-L173'
  - symbol: encode
    kind: function
    at: 'scripts/ops/airtable-read.py:L176-L183'
  - symbol: to_body
    kind: function
    at: 'scripts/ops/airtable-read.py:L186-L198'
  - symbol: request
    kind: function
    at: 'scripts/ops/airtable-read.py:L201-L217'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/airtable-read.py:L220-L239'
  - symbol: clip
    kind: function
    at: 'scripts/ops/airtable-read.py:L242-L248'
  - symbol: main
    kind: function
    at: 'scripts/ops/airtable-read.py:L251-L343'
---
<!-- context:generated:start -->
## Summary

The wrapper that gates Airtable reads to control context costs: unscoped reads are refused, --all-fields and --max-records are capped, pageSize never exceeds 100, and record IDs become an OR(RECORD_ID()=...) formula combined with --formula via AND. Its --print-query mode makes the query-shaping logic testable fully offline.

## Related

- uses [[airtable-ops-watchers]] — Watchers paginate records through this wrapper's scoping conventions.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
