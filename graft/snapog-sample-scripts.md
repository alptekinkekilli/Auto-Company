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
  - to: snapog-cost-alerts
    relation: validates
    description: alerts-dry-run.sh verifies the cron alert pipeline fires.
  - to: snapog-worker
    relation: validates
    description: Smoke-tests the /og endpoint and cache-cap behavior.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

One-off validation scripts for specific fixes rather than maintained tests: smoke-test.sh (basic /health and /og PNG check), cache-cap-test.sh (verifies X-Cache: BYPASSED after MONTHLY_CACHE_KEY_CAP distinct keys), and alerts-dry-run.sh (seeds 500 cache-miss rows via recursive CTE and triggers the cron handler via /__scheduled to verify alert firing without real webhooks).

## Related

- validates [[snapog-cost-alerts]] — alerts-dry-run.sh verifies the cron alert pipeline fires.
- validates [[snapog-worker]] — Smoke-tests the /og endpoint and cache-cap behavior.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
