---
name: Auto Company loop core
slug: auto-company-loop-core
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
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
sources_digest: b8b1e8ec0b12b29cb418920d6bdf66ac73aca8c61d04640f616839d0007309e7
links:
  - to: final-text-extraction
    relation: uses
    description: >-
      auto-loop.sh falls back to raw file content when final_text returns exit 1
      (no agent message).
  - to: operator-escalation-gate
    relation: uses
    description: >-
      Loop calls operator_request_notify.py to gate OPREQ notifications and
      projection.
  - to: telegram-notification
    relation: uses
    description: Loop and its helpers send operator alerts via telegram-notify.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central background loop that runs cycles of the Auto Company agent, orchestrated by auto-loop.sh and its helpers. It reads state files (.auto-loop-state, .auto-loop.pid, .auto-loop-paused), writes logs under logs/, and is managed by stop-loop.sh, monitor.sh, and the macOS/container status scripts. The loop is the consumer of most ops scripts' outputs and the producer of the audit trail (auto-loop.log, cycle-ndjson).

## Related

- uses [[final-text-extraction]] — auto-loop.sh falls back to raw file content when final_text returns exit 1 (no agent message).
- uses [[operator-escalation-gate]] — Loop calls operator_request_notify.py to gate OPREQ notifications and projection.
- uses [[telegram-notification]] — Loop and its helpers send operator alerts via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
