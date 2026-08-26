---
name: SnapOG Smoke Tests
slug: snapog-smoke-tests
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
  - to: snapog-worker
    relation: validates
    description: 'Smoke tests verify the /og endpoint, cache-cap behavior, and alert cron.'
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

One-off Bash validation scripts for specific SnapOG fixes, archived under _archive/snapog/sample/. smoke-test.sh checks /health and /og PNG size; cache-cap-test.sh verifies that after MONTHLY_CACHE_KEY_CAP distinct keys the R2 cache returns X-Cache: BYPASSED; alerts-dry-run.sh seeds 500 cache-miss rows and triggers the /__scheduled cron to verify alert logic without real webhooks.

## Related

- validates [[snapog-worker]] — Smoke tests verify the /og endpoint, cache-cap behavior, and alert cron.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
