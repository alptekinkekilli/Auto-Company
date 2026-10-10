---
name: Infrastructure & Ops Guards
slug: infrastructure-ops-guards
type: system
sources:
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 8451d15f3a072166e7b153777dc4b1d55f049abdc3fe3f2f209dfc9a256ac39c
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Host-level operational guards and scheduled jobs. docker-prune-safe.sh is a threshold-gated disk guard (WARN runs non-destructive builder/image prune; THRESH additionally prunes stopped containers older than 24h; volumes never touched) that notifies by piping into the running container to avoid dot-sourcing env with `|` values. sentry-heartbeat.sh proves the process tree is alive via Sentry Crons, reporting error immediately on any liveness failure to catch crash-loops. opportunity-analyst-cron.sh is the daily APP-221 cron entry, selecting engine, enforcing a codex-idle guard, and reporting to Sentry. operator-usage-report.sh pushes operator Claude usage into the container for calibration.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
