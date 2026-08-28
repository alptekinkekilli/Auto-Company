---
name: stop-loop
slug: stop-loop
type: file
sources:
  - path: scripts/core/stop-loop.sh
    hash: 4ea7f4b5ce31ce14039bf5cedd3c6a9718e2357906fe289906d06debe11f3fe3
sources_digest: f8bc188b35a32ae2582e0772ca6b3d845905b928533499e9401b86774db72895
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Graceful shutdown for the background loop. Two modes: signal file (.auto-loop-stop) + optional SIGTERM for foreground; pause/resume macOS launchd daemon. Two-pronged stop (signal for graceful cycle completion plus SIGTERM immediate). Idempotent stale PID cleanup.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
