---
name: HeadInspect Privacy Invariant
slug: headinspect-privacy-invariant
type: concept
sources:
  - path: projects/headinspect/migrations/0001_hits.sql
    hash: 651c37d5aafbcd41932f5307a9080183fd953c8b5968f3dd2921bf1c379af022
sources_digest: 749d2c2597b768efd8b2d98fa11448a3fea8bb6aa07962bec8ae443dd5bd793b
links:
  - to: headinspect-service
    relation: part_of
    description: The migration defines the schema the service's hit counter writes to.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The anonymous hit counter stores only the hostname, never the full URL, to prevent query strings from leaking personally identifiable information. The binding is intentionally left out of wrangler.toml, requiring a one-line uncomment to enable. checked_at is stored as ISO-8601 text rather than a native timestamp.

## Related

- part of [[headinspect-service]] — The migration defines the schema the service's hit counter writes to.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
