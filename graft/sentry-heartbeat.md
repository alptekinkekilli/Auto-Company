---
name: Sentry heartbeat
slug: sentry-heartbeat
type: file
sources:
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
sources_digest: 478d093a57b8382e12406ee9572a739f3d97a5ae5f0b9987559cfeb7682ede19
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Background heartbeat for Sentry Crons proving the container process tree is alive independently of the dashboard or loop cycle, specifically to catch crash-loops (APP-250) that app-level error reporting misses. Only reports 'ok' if BOTH the dashboard /api/status and the loop PID are alive (to avoid false positives during restart storms, APP-240), reports 'error' immediately otherwise, and is strictly best-effort with an 8s startup grace window.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
