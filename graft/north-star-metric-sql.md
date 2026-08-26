---
name: North-Star Metric SQL
slug: north-star-metric-sql
type: file
sources:
  - path: docs/operations/north-star-metric-query.sql
    hash: 0ef7a67fdb263a3fb09f795cc5a35372721265b7ef1f6200c5ccc369109f7ac6
sources_digest: 91dcfb3b617798695902ce25230879b0ebdf6c4ac53fe80d36c1db48d76a29a9
links:
  - to: snapog-service
    relation: validates
    description: Queries the usage_events/api_keys schema defined by the SnapOG migrations.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Canonical SQL for SnapOG's north-star metric Weekly Active Producers (WAP), counting distinct api_key_id values that generated at least one non-cached OG image within a window. Cache hits are excluded because they represent edge-served static responses with near-zero marginal cost and no signal of new demand. Days with zero traffic produce no rows (zero-filling must happen client-side); queries are safe to run from the dashboard, wrangler d1 execute, or the Cloudflare MCP tool.

## Related

- validates [[snapog-service]] — Queries the usage_events/api_keys schema defined by the SnapOG migrations.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
