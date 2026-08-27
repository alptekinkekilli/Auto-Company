---
name: SnapOG North-Star Metric SQL
slug: snapog-north-star-metric-sql
type: file
sources:
  - path: docs/operations/north-star-metric-query.sql
    hash: 0ef7a67fdb263a3fb09f795cc5a35372721265b7ef1f6200c5ccc369109f7ac6
sources_digest: 91dcfb3b617798695902ce25230879b0ebdf6c4ac53fe80d36c1db48d76a29a9
links:
  - to: snapog-og-image-service
    relation: validates
    description: >-
      Queries the snapog-db D1 database whose schema comes from
      migrations/0001_init.sql.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Canonical SQL for the Weekly Active Producers (WAP) north-star metric, counting distinct api_key_id values that generated at least one non-cached OG image within a window. Cache hits are deliberately excluded because they represent edge-served static responses with near-zero marginal cost and no signal of new demand. Days with zero traffic produce no rows, so zero-filling must happen client-side.

## Related

- validates [[snapog-og-image-service]] — Queries the snapog-db D1 database whose schema comes from migrations/0001_init.sql.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
