---
name: Infrastructure and host hygiene
slug: infrastructure-and-host-hygiene
type: system
sources:
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 26344e500472e6d9b4d4c77c49cffb46d4943a9409627a106209825760e57677
links:
  - to: telegram-notification
    relation: uses
    description: docker-prune-safe.sh and sentry-heartbeat.sh notify via Telegram.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Host-level operational guards: docker-prune-safe.sh is a threshold-gated disk guard that never touches volumes and keeps recently-stopped containers for debugging; sentry-heartbeat.sh proves the container process tree is alive independently of the dashboard to catch crash-loops; opportunity-analyst-cron.sh is the daily cron entry for the Opportunity Analyst with a codex-idle guard and rollback path.

## Related

- uses [[telegram-notification]] — docker-prune-safe.sh and sentry-heartbeat.sh notify via Telegram.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
