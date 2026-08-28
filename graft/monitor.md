---
name: monitor
slug: monitor
type: file
sources:
  - path: scripts/core/monitor.sh
    hash: 9a104b2efb99c2712cbff51c614b1dc964f3a8be29ba7bc990c3d63d7c58bd03
sources_digest: 6a4e61f49712a799801edf2ac66fb4e4f77a1270a69941231971467bf2ab54f3
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Live monitoring interface for the Auto Company loop: tail main log, status, latest cycle, cycle history. Reads PID file, pause flag, state file, logs, consensus memory. Detects host platform (systemctl --user vs launchctl) for daemon health.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
