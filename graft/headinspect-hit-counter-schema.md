---
name: HeadInspect Hit Counter Schema
slug: headinspect-hit-counter-schema
type: file
sources:
  - path: projects/headinspect/migrations/0001_hits.sql
    hash: 651c37d5aafbcd41932f5307a9080183fd953c8b5968f3dd2921bf1c379af022
sources_digest: 749d2c2597b768efd8b2d98fa11448a3fea8bb6aa07962bec8ae443dd5bd793b
links:
  - to: headinspect-header-inspector
    relation: part_of
    description: Schema backing the worker's hit counter.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

SQLite/D1 schema for the anonymous hit counter. Only the hostname is stored, never the full URL, to prevent query strings from leaking PII; checked_at is stored as ISO-8601 text. The binding is intentionally left out of wrangler.toml and requires a one-line uncomment to enable.

## Related

- part of [[headinspect-header-inspector]] — Schema backing the worker's hit counter.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
