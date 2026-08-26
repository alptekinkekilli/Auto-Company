---
name: SnapOG Schema
slug: snapog-schema
type: system
sources:
  - path: projects/_archive/snapog/migrations/0001_init.sql
    hash: 5a2ecc41dbff948e5d8f895feb80ae4145864f3703776f737cda73c84fec8623
  - path: projects/_archive/snapog/migrations/0002_waitlist.sql
    hash: 541f4f76f6f87aab342fe067acbcc746587f600d1e76028fe97a4c67c8b3202a
  - path: projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
    hash: a672bc9c2f87bedb83312ef869d3ea29305f96bcca7241131ce1130edcb4ee75
sources_digest: 8820226ce02d1d9ebb352867760d54a674115efb44b492597558e611bb10dc93
links:
  - to: snapog-worker
    relation: implements
    description: Schema the Worker persists against.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

D1 schema for SnapOG: users, api_keys (display-only key_prefix + SHA-256 key_hash, tier, monthly quota, usage_reset_at), usage_events, waitlist, and api_key_cache_keys (composite PK on key/cache_key/billing_month for R2 storage-abuse tracking). Deliberately avoids storing raw keys; billing-month boundaries tie to api_keys.usage_reset_at semantics to avoid double-counting.

## Related

- implements [[snapog-worker]] — Schema the Worker persists against.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
