---
name: Loop lifecycle & monitoring (core shell)
slug: loop-lifecycle-monitoring-core-shell
type: system
sources:
  - path: scripts/core/monitor.sh
    hash: 9a104b2efb99c2712cbff51c614b1dc964f3a8be29ba7bc990c3d63d7c58bd03
  - path: scripts/core/stop-loop.sh
    hash: 4ea7f4b5ce31ce14039bf5cedd3c6a9718e2357906fe289906d06debe11f3fe3
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
sources_digest: 3754675e96be04f98ef14bfdea09eb7ec93cb9d200ec9d484544c1fd44b934f3
links:
  - to: auto-loop-orchestration
    relation: uses
    description: >-
      stop-loop.sh writes .auto-loop-stop and .auto-loop-paused signals that
      auto-loop.sh and the launchd daemon honor.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash utilities around the Auto Company background loop: monitor.sh (live tail/status/cycles view reading PID, pause flag, state file, consensus), stop-loop.sh (graceful stop via .auto-loop-stop signal file plus SIGTERM, and macOS launchd pause/resume via --pause-daemon/--resume-daemon), and telegram-notify.sh (safe-to-call-unconditionally Telegram sender that exits silently when creds unset, truncates to 3900 chars, never returns non-zero). These coordinate the loop's lifecycle and operator notification without ever breaking a caller.

## Related

- uses [[auto-loop-orchestration]] — stop-loop.sh writes .auto-loop-stop and .auto-loop-paused signals that auto-loop.sh and the launchd daemon honor.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
