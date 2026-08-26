---
name: Loop Lifecycle & Monitoring
slug: loop-lifecycle-monitoring
type: system
sources:
  - path: scripts/core/monitor.sh
    hash: 9a104b2efb99c2712cbff51c614b1dc964f3a8be29ba7bc990c3d63d7c58bd03
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
  - path: scripts/core/stop-loop.sh
    hash: 4ea7f4b5ce31ce14039bf5cedd3c6a9718e2357906fe289906d06debe11f3fe3
sources_digest: de3a4d542bf8fb9c655ec4e27c2ef95092a2da94fd27c6740380b87e8ffab8d8
links:
  - to: platform-status-scripts
    relation: uses
    description: >-
      monitor.sh and status scripts read the same runtime artifacts
      (.auto-loop.pid, .auto-loop-state, logs/).
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Manages and observes the background Auto Company loop. stop-loop.sh provides graceful shutdown (signal file plus SIGTERM, pause/resume flags), monitor.sh tails logs and reports daemon health via systemctl/launchctl, and sentry-heartbeat.sh proves the process tree is alive independently of the dashboard to catch crash-loops (APP-250), only reporting ok when both dashboard and loop PID are alive to avoid false positives during restart storms (APP-240).

## Related

- uses [[platform-status-scripts]] — monitor.sh and status scripts read the same runtime artifacts (.auto-loop.pid, .auto-loop-state, logs/).
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
