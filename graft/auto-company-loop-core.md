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
  - to: directive-writer
    relation: uses
    description: >-
      The loop's directive handling is gated by directive_writer.py's
      fail-closed rules.
  - to: engine-final-text-extraction
    relation: uses
    description: >-
      auto-loop.sh falls back to raw file content when codex-final-text.py
      returns exit 1 (no agent message).
  - to: telegram-notification
    relation: uses
    description: The loop and its helpers send operator alerts via telegram-notify.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central background loop that runs cycles of the Auto Company agent, orchestrating engine invocation, state files, pause/stop signals, and cycle lifecycle. It is the process that all the scripts in scripts/core support, and it is managed by launchd (macOS) or the container runtime (Coolify).

## Related

- uses [[directive-writer]] — The loop's directive handling is gated by directive_writer.py's fail-closed rules.
- uses [[engine-final-text-extraction]] — auto-loop.sh falls back to raw file content when codex-final-text.py returns exit 1 (no agent message).
- uses [[telegram-notification]] — The loop and its helpers send operator alerts via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
