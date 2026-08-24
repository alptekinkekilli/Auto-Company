---
name: SnapOG schema & waitlist
slug: snapog-schema-waitlist
type: system
sources:
  - path: docs/operations/north-star-metric-query.sql
    hash: 0ef7a67fdb263a3fb09f795cc5a35372721265b7ef1f6200c5ccc369109f7ac6
  - path: projects/_archive/snapog-landing/functions/api/waitlist.ts
    hash: 49b5d66187a49f386d4bee50c1c01042d595e5ebbd5b27c061f1fba4cffeefa0
  - path: projects/_archive/snapog/migrations/0001_init.sql
    hash: 5a2ecc41dbff948e5d8f895feb80ae4145864f3703776f737cda73c84fec8623
  - path: projects/_archive/snapog/migrations/0002_waitlist.sql
    hash: 541f4f76f6f87aab342fe067acbcc746587f600d1e76028fe97a4c67c8b3202a
  - path: projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
    hash: a672bc9c2f87bedb83312ef869d3ea29305f96bcca7241131ce1130edcb4ee75
sources_digest: e3008462b75195f4275d8a4c60696876b06033d7548a78343388471d159f023c
links:
  - to: snapog-og-image-service
    relation: implements
    description: Provides the persistence layer the worker reads/writes.
generator:
  version: 1
covers:
  - symbol: Env
    kind: interface
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L12-L14'
  - symbol: Body
    kind: interface
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L16-L20'
  - symbol: onRequestPost
    kind: function
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L24-L62'
  - symbol: json
    kind: function
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L64-L72'
---
<!-- context:generated:start -->
## Summary

D1 schema: users, api_keys (hash-only, no raw keys), usage_events, waitlist, and api_key_cache_keys for R2 abuse tracking. Billing-month boundaries tied to api_keys.usage_reset_at; cache hits excluded from WAP north-star metric.

## Related

- implements [[snapog-og-image-service]] — Provides the persistence layer the worker reads/writes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
