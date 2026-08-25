---
name: loop lifecycle & monitoring
slug: loop-lifecycle-monitoring
type: system
sources:
  - path: scripts/core/monitor.sh
    hash: 9a104b2efb99c2712cbff51c614b1dc964f3a8be29ba7bc990c3d63d7c58bd03
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
  - path: scripts/core/stop-loop.sh
    hash: 4ea7f4b5ce31ce14039bf5cedd3c6a9718e2357906fe289906d06debe11f3fe3
  - path: scripts/linux/noop-action.sh
    hash: 0f0aaa7c6c79e6c7844c7528a253084811b9a9b7277f557a1a60a8011347f4d9
  - path: scripts/linux/status-linux.sh
    hash: 1dc4a455fe8ffdd5e1696608d50d02311afd701906d80ee26d5708374d3947d8
  - path: scripts/macos/status-mac.sh
    hash: ba8bc08141ca80245bea6ccb35984221942d6a855ce856e5a492a38c4c151418
sources_digest: f880e71455c50baed0b45c470cb71718ba08261b03ed3e9ba876f142465c9baf
links:
  - to: macos-daemon-install
    relation: uses
    description: >-
      status-mac and monitor inspect the launchd LaunchAgent installed by
      install-daemon.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash scripts that manage and observe the background auto-loop: graceful stop, live monitor, sentry heartbeat, and platform-specific status reports. Coordinate via shared runtime artifacts (.auto-loop.pid, .auto-loop-paused, .auto-loop-state) and the consensus memory file.

## Related

- uses [[macos-daemon-install]] — status-mac and monitor inspect the launchd LaunchAgent installed by install-daemon.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
