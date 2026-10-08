---
name: Sentry heartbeat
slug: sentry-heartbeat
type: system
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

Background Sentry Crons heartbeat proving the container process tree is alive independently of the dashboard or loop cycle, specifically to catch crash-loops (APP-250) that application-level error reporting misses. Only reports 'ok' if BOTH dashboard /api/status and loop PID are alive, reporting 'error' immediately otherwise to avoid false positives during fast restart storms (APP-240). Strictly best-effort with an 8s startup grace window.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
