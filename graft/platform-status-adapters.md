---
name: Platform status adapters
slug: platform-status-adapters
type: system
sources:
  - path: scripts/linux/noop-action.sh
    hash: 0f0aaa7c6c79e6c7844c7528a253084811b9a9b7277f557a1a60a8011347f4d9
  - path: scripts/linux/status-linux.sh
    hash: 1dc4a455fe8ffdd5e1696608d50d02311afd701906d80ee26d5708374d3947d8
  - path: scripts/macos/install-daemon.sh
    hash: 21f1e9576d7552530f20812f04232c75a2dadb4a7f5e3819045a35dec10037e9
  - path: scripts/macos/status-mac.sh
    hash: ba8bc08141ca80245bea6ccb35984221942d6a855ce856e5a492a38c4c151418
sources_digest: f255c43465d62dbf3f2557bb92ba24462856a6cb2e41ab0f71ef970cddecdb31
links:
  - to: loop-monitoring-and-lifecycle
    relation: uses
    description: >-
      Both status scripts read the same PID/state/consensus/log artifacts;
      install-daemon.sh manages the launchd daemon that stop-loop.sh
      pauses/resumes.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Two platform-specific status reporters emitting the same '=== Section ===' + Key=Value format the dashboard parses: status-mac.sh checks Guardian (caffeinate), launchd Daemon, Autostart, Loop, and dumps state/consensus/logs; status-linux.sh is container-adapted, marking the sleep guard not_applicable and assuming Coolify restart policy. noop-action.sh is a placeholder for Start/Stop controls in container mode so the dashboard never attempts macOS/launchd actions.

## Related

- uses [[loop-monitoring-and-lifecycle]] — Both status scripts read the same PID/state/consensus/log artifacts; install-daemon.sh manages the launchd daemon that stop-loop.sh pauses/resumes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
