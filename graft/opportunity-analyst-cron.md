---
name: Opportunity Analyst cron
slug: opportunity-analyst-cron
type: system
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: c9528c3c886526e331f350d771be52e2e29ed85299416da9b337599e373180c9
sources_digest: 598186fea5b3f94add7c555b80936614ca3a51ff9c8eb67cd658783fd562ca23
links:
  - to: cost-budget-calibration
    relation: uses
    description: >-
      Runs before the cost-audit so the analyst interprets measured numbers
      rather than re-deriving them.
  - to: loop-lifecycle-monitoring
    relation: uses
    description: >-
      Reports liveness to Sentry Crons and waits for the company loop to be
      free.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry point for the Opportunity Analyst job, selecting between a legacy codex rollback path and the default jcode one-shot pilot container. Includes a codex-idle guard, image-pruning fallback, refresh of scripts/tests/framework from the live prod container, and validation for REPORT_OK and 'registry: skipped' markers, treating a skipped day as a liveness failure.

## Related

- uses [[cost-budget-calibration]] — Runs before the cost-audit so the analyst interprets measured numbers rather than re-deriving them.
- uses [[loop-lifecycle-monitoring]] — Reports liveness to Sentry Crons and waits for the company loop to be free.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
