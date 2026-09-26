---
name: Loop lifecycle and monitoring
slug: loop-lifecycle-and-monitoring
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
    relation: part_of
    description: These scripts manage and observe the auto-loop process.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash scripts managing the Auto Company background loop: graceful stop (signal file for graceful cycle completion plus SIGTERM, pause/resume macOS launchd daemon), live monitoring (tail log, status, cycle history, daemon health via systemctl/launchctl), and a Sentry Crons heartbeat proving the process tree is alive independently of the dashboard (catches crash-loops APP-250 that app-level error reporting misses; only reports ok if both dashboard and loop PID are alive to avoid false positives during restart storms).

## Related

- part of [[auto-loop-orchestration]] — These scripts manage and observe the auto-loop process.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
