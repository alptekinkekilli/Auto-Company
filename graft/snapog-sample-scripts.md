---
name: SnapOG Sample Scripts
slug: snapog-sample-scripts
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
    description: Smoke-test and cache-cap behavior of the /og endpoint and cron alerting.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

One-off operational validation scripts for the archived SnapOG service: a smoke test of /health and /og, a dry-run of the cost-alert cron against a local Wrangler dev server (seeding 500 cache-miss rows to trip the 14-day hit-rate threshold), and a cache-cap test verifying that after MONTHLY_CACHE_KEY_CAP distinct keys the R2 cache returns X-Cache: BYPASSED. These are manual/CI checks, not maintained unit tests, and write throwaway rows into local Miniflare D1 state.

## Related

- validates [[snapog-service]] — Smoke-test and cache-cap behavior of the /og endpoint and cron alerting.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
