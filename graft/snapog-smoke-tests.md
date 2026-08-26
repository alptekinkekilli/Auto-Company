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
  - to: snapog-cost-alerts
    relation: validates
    description: alerts-dry-run.sh verifies alert logic fires without real webhooks.
  - to: snapog-worker
    relation: validates
    description: Smoke tests verify worker behavior including cache-cap bypass.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Archived one-off validation scripts for SnapOG fixes: smoke-test.sh (health + /og PNG size check), cache-cap-test.sh (verifies X-Cache: BYPASSED after MONTHLY_CACHE_KEY_CAP distinct keys), alerts-dry-run.sh (seeds 500 cache-miss rows to trip 14-day hit-rate threshold, triggers /__scheduled, expects log lines). Write throwaway rows into local Miniflare D1 state resettable by deleting .wrangler/state/v3/d1.

## Related

- validates [[snapog-cost-alerts]] — alerts-dry-run.sh verifies alert logic fires without real webhooks.
- validates [[snapog-worker]] — Smoke tests verify worker behavior including cache-cap bypass.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
