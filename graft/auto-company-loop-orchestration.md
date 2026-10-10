---
name: Auto Company Loop Orchestration
slug: auto-company-loop-orchestration
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
  - to: operator-escalation-notification
    relation: uses
    description: >-
      monitor.sh and status scripts read consensus.md and state files that
      operator_request_notify.py also maintains
  - to: runtime-env-secret-handling
    relation: uses
    description: >-
      status scripts and daemon read runtime.env and state files for credentials
      and configuration
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The background automation loop that runs cycles of the Auto Company agent, with lifecycle management across macOS (launchd daemon, caffeinate guardian) and Linux/container (Coolify) runtimes. Includes graceful shutdown via signal file + SIGTERM, pause coordination, and a live monitoring interface for operators. The loop is the main process in container mode and a launchd LaunchAgent on macOS, with KeepAlive tied to a pause flag.

## Related

- uses [[operator-escalation-notification]] — monitor.sh and status scripts read consensus.md and state files that operator_request_notify.py also maintains
- uses [[runtime-env-secret-handling]] — status scripts and daemon read runtime.env and state files for credentials and configuration
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
