---
name: SnapOG Schema
slug: snapog-schema
type: system
sources:
  - path: docs/operations/north-star-metric-query.sql
    hash: 0ef7a67fdb263a3fb09f795cc5a35372721265b7ef1f6200c5ccc369109f7ac6
  - path: projects/_archive/snapog/migrations/0001_init.sql
    hash: 5a2ecc41dbff948e5d8f895feb80ae4145864f3703776f737cda73c84fec8623
  - path: projects/_archive/snapog/migrations/0002_waitlist.sql
    hash: 541f4f76f6f87aab342fe067acbcc746587f600d1e76028fe97a4c67c8b3202a
  - path: projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
    hash: a672bc9c2f87bedb83312ef869d3ea29305f96bcca7241131ce1130edcb4ee75
sources_digest: 4429fc0619a4d35d793b67da0db3586621b19ca762a52cc8ebe57e0fa264127b
links:
  - to: snapog-worker
    relation: uses
    description: >-
      The worker reads/writes these tables for auth, usage, and cache-key
      tracking.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

D1 schema for SnapOG: users, api_keys (key_prefix + SHA-256 key_hash, never raw keys), usage_events, waitlist, and api_key_cache_keys tracking distinct cache keys per key per billing month (G8 R2 storage abuse fix). Billing-month boundaries tied to api_keys.usage_reset_at semantics; no foreign keys enforced. The north-star WAP query excludes cache hits because they represent edge-served static responses with near-zero marginal cost.

## Related

- uses [[snapog-worker]] — The worker reads/writes these tables for auth, usage, and cache-key tracking.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
