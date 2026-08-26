---
name: loop lifecycle & monitoring
slug: loop-lifecycle-monitoring
type: system
sources:
  - path: scripts/core/monitor.sh
    hash: 9a104b2efb99c2712cbff51c614b1dc964f3a8be29ba7bc990c3d63d7c58bd03
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
sources_digest: fd274d10c1ef9d3ff84ad7606b981bb66736c539a7dddfcccf1aac918ac8d0ff
links:
  - to: operator-escalation-gate
    relation: uses
    description: >-
      monitor.sh and status scripts read consensus.md and the state file that
      the escalation gate writes.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Graceful start/stop, pause/resume, and live monitoring of the background Auto Company loop across macOS (launchd) and container (Coolify) runtimes. Stop uses a two-pronged approach (signal file for graceful cycle completion plus SIGTERM), pause is coordinated via a .auto-loop-paused flag that launchd KeepAlive honors, and monitoring reads runtime artifacts (PID, state, consensus, logs) with OS-specific daemon health checks. Container mode deliberately no-ops lifecycle actions so the dashboard never reports false failures.

## Related

- uses [[operator-escalation-gate]] — monitor.sh and status scripts read consensus.md and the state file that the escalation gate writes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
