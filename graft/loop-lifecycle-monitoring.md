---
name: Loop lifecycle & monitoring
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
  - path: scripts/macos/install-daemon.sh
    hash: 21f1e9576d7552530f20812f04232c75a2dadb4a7f5e3819045a35dec10037e9
  - path: scripts/macos/status-mac.sh
    hash: ba8bc08141ca80245bea6ccb35984221942d6a855ce856e5a492a38c4c151418
sources_digest: 70f5124c9f4a6e9fe9a49ad0f8ac9841733a80e231959a056c0bf40e73807226
links:
  - to: cost-budget-calibration
    relation: produces
    description: >-
      The loop's logs and state files are the inputs the cost-audit and
      budget-calibration scripts parse.
  - to: operator-escalation-notification
    relation: uses
    description: >-
      Sentry heartbeat and status reports feed the same operator-facing
      channels.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The background-loop control plane: graceful stop (signal file plus SIGTERM), pause/resume of the macOS launchd daemon, live operator monitoring (status, last cycle, cycle history), and a Sentry heartbeat that proves the process tree is alive to catch crash-loops that app-level error reporting misses. Platform-specific status scripts emit the same Key=Value format the dashboard parses, with the Linux/container variant marking sleep guard not_applicable and deferring lifecycle to Coolify.

## Related

- produces [[cost-budget-calibration]] — The loop's logs and state files are the inputs the cost-audit and budget-calibration scripts parse.
- uses [[operator-escalation-notification]] — Sentry heartbeat and status reports feed the same operator-facing channels.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
