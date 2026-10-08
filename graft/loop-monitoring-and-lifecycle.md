---
name: Loop monitoring and lifecycle
slug: loop-monitoring-and-lifecycle
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
  - to: auto-loop-orchestration
    relation: uses
    description: >-
      Reads and writes the loop's PID file, pause flag, state file, and logs;
      sentry-heartbeat is started by docker-entrypoint.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash tooling for observing and controlling the Auto Company background loop: monitor.sh tails logs and reports loop/daemon/state/consensus status with OS-specific daemon checks; stop-loop.sh provides graceful shutdown via signal file plus SIGTERM, and pause/resume of the macOS launchd daemon via a .auto-loop-paused flag; sentry-heartbeat.sh proves the container process tree is alive independently of the dashboard, reporting error immediately unless both dashboard and loop PID are alive to avoid false positives during restart storms.

## Related

- uses [[auto-loop-orchestration]] — Reads and writes the loop's PID file, pause flag, state file, and logs; sentry-heartbeat is started by docker-entrypoint.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
