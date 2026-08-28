---
name: sentry-heartbeat
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

Background heartbeat for Sentry Crons proving container process tree alive, catching crash-loops (APP-250) app-level error reporting misses. Verifies dashboard /api/status and loop PID liveness, 90s loop posting ok/error. Best-effort (|| true), 8s startup grace, only reports ok if both dashboard and loop PID alive to avoid false positives during restart storms (APP-240).
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
