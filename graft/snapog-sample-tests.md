---
name: SnapOG Sample Tests
slug: snapog-sample-tests
type: system
sources:
  - path: projects/_archive/snapog/sample/alerts-dry-run.sh
    hash: fabd322c673a2e7f93273116221eac10392cdbf3d6cd8eb5457e6c960b67797c
  - path: projects/_archive/snapog/sample/cache-cap-test.sh
    hash: c11830b054136c0d367415ca1a62bc16312be6ec69c45fc217b2fda9bf8a67bc
  - path: projects/_archive/snapog/sample/smoke-test.sh
    hash: 0a140d23218574add9c22c524d6ff03aea85a205f4806261fc0791a4b73c144f
sources_digest: ce9cb2a773c1290423006a58fe8d649723cb56a07022127ba072ed0d87b79c56
links:
  - to: snapog-service
    relation: validates
    description: 'Exercise the /og endpoint, cache-cap behavior, and cost-alert cron.'
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

One-off validation scripts for specific SnapOG fixes, archived under _archive/snapog/sample/: a smoke test for the /health and /og endpoints, a dry-run of the cost-alert cron against a local Wrangler dev server (seeding 500 cache-miss rows to trip the 14-day threshold), and a per-key cache-cap test asserting R2 returns X-Cache: BYPASSED after the cap. These are operational checks, not maintained unit tests.

## Related

- validates [[snapog-service]] — Exercise the /og endpoint, cache-cap behavior, and cost-alert cron.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
