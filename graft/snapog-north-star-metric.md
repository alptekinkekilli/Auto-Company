---
name: SnapOG North-Star Metric
slug: snapog-north-star-metric
type: concept
sources:
  - path: docs/operations/north-star-metric-query.sql
    hash: 0ef7a67fdb263a3fb09f795cc5a35372721265b7ef1f6200c5ccc369109f7ac6
  - path: projects/_archive/snapog/migrations/0001_init.sql
    hash: 5a2ecc41dbff948e5d8f895feb80ae4145864f3703776f737cda73c84fec8623
sources_digest: 5a85f505c12c27179b28ca0f4cca585823fb776a4407a955dc28d492b38e41fc
links:
  - to: snapog-og-image-service
    relation: validates
    description: Queries the usage_events/api_keys schema the service maintains
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Weekly Active Producers (WAP) — the canonical north-star metric counting distinct api_key_id values that generated at least one non-cached OG image (cache_hit=0) within a reporting window. Cache hits are deliberately excluded because they represent edge-served static responses with near-zero marginal cost and no signal of new demand; only cache misses indicate real load-bearing generation. Three read-only queries: daily 30-day time-series, 7/30-day scorecard rollups, and a per-key leaderboard joining usage_events to api_keys for testimonial candidates and free-tier keys nearing monthly_limit. Days with zero traffic produce no rows — zero-filling must happen client-side.

## Related

- validates [[snapog-og-image-service]] — Queries the usage_events/api_keys schema the service maintains
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
