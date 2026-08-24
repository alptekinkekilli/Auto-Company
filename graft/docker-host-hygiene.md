---
name: Docker & host hygiene
slug: docker-host-hygiene
type: system
sources:
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: c9528c3c886526e331f350d771be52e2e29ed85299416da9b337599e373180c9
sources_digest: 1c7e360b4692ca19c7c949b04336c509aba8b26ca2b7f424e516db94cd68b025
links:
  - to: loop-lifecycle-monitoring-shell
    relation: uses
    description: >-
      opportunity-analyst-cron reports liveness to Sentry Crons like
      sentry-heartbeat.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Threshold-gated Docker disk guard (WARN runs only non-destructive prunes so crash evidence survives; THRESH additionally prunes stopped containers; volumes never touched) and the daily Opportunity Analyst cron that orchestrates a one-shot jcode pilot container, mirroring scripts/tests/framework from the prod container and treating a skipped day as a liveness failure.

## Related

- uses [[loop-lifecycle-monitoring-shell]] — opportunity-analyst-cron reports liveness to Sentry Crons like sentry-heartbeat.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
