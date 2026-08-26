---
name: HeadInspect Schema
slug: headinspect-schema
type: file
sources:
  - path: projects/headinspect/migrations/0001_hits.sql
    hash: 651c37d5aafbcd41932f5307a9080183fd953c8b5968f3dd2921bf1c379af022
sources_digest: 749d2c2597b768efd8b2d98fa11448a3fea8bb6aa07962bec8ae443dd5bd793b
links:
  - to: headinspect-worker
    relation: implements
    description: Defines the persistence layer for hit counting.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Migration for the anonymous hit counter: headinspect_hits table with auto-increment id, ISO-8601 checked_at, and host. Only the hostname is stored, never the full URL, to prevent query strings leaking PII. The D1 binding is intentionally left out of wrangler.toml — enabling requires a one-line uncomment.

## Related

- implements [[headinspect-worker]] — Defines the persistence layer for hit counting.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
