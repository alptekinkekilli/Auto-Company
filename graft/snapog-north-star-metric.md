---
name: SnapOG North-Star Metric
slug: snapog-north-star-metric
type: file
sources:
  - path: docs/operations/north-star-metric-query.sql
    hash: 0ef7a67fdb263a3fb09f795cc5a35372721265b7ef1f6200c5ccc369109f7ac6
sources_digest: 91dcfb3b617798695902ce25230879b0ebdf6c4ac53fe80d36c1db48d76a29a9
links:
  - to: snapog-service
    relation: validates
    description: >-
      Queries the same D1 schema (migrations/0001_init.sql) that the Worker
      writes.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Canonical SQL for Weekly Active Producers (WAP), counting distinct api_key_id values with at least one non-cached OG image (cache_hit=0) in a window. Cache hits are deliberately excluded because they represent edge-served static responses with near-zero marginal cost. Three read-only queries: daily 30-day time-series, 7/30-day scorecards, and a per-key leaderboard for testimonial candidates and free-tier keys nearing monthly_limit. Days with zero traffic produce no rows (zero-fill client-side).

## Related

- validates [[snapog-service]] — Queries the same D1 schema (migrations/0001_init.sql) that the Worker writes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
