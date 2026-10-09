---
name: Sentry heartbeat & crash-loop detection
slug: sentry-heartbeat-crash-loop-detection
type: system
sources:
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: bf5b5c828a4a386d38abc121e6c8299b54474a9ae09c8400479a6ca1629be2d9
links:
  - to: loop-lifecycle-monitoring
    relation: uses
    description: Heartbeat reads the loop PID file and dashboard status to judge liveness.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

sentry-heartbeat.sh proves the container process tree is alive independently of the dashboard or loop cycle, specifically to catch crash-loops (APP-250) that app-level error reporting misses. It only reports 'ok' if both the dashboard /api/status and the loop PID are alive, and reports 'error' immediately otherwise, bypassing the missed-checkin margin to avoid false positives during fast restart storms (APP-240). opportunity-analyst-cron.sh also reports liveness to Sentry Crons with in_progress/ok/error statuses.

## Related

- uses [[loop-lifecycle-monitoring]] — Heartbeat reads the loop PID file and dashboard status to judge liveness.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
