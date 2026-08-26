---
name: Platform Status Scripts
slug: platform-status-scripts
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
  - to: loop-lifecycle-monitoring
    relation: uses
    description: >-
      Status scripts read the same runtime artifacts and daemon state the loop
      writes.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Platform-specific status reporters for the dashboard. status-mac.sh and status-linux.sh emit the same '=== Section ===' + Key=Value format that parse_macos_status_output in dashboard/server.py expects; the Linux variant marks the sleep guard not_applicable and assumes Coolify restart policy. install-daemon.sh generates a launchd plist with KeepAlive tied to the .auto-loop-paused flag. noop-action.sh is a placeholder so the container dashboard never attempts macOS/launchd actions.

## Related

- uses [[loop-lifecycle-monitoring]] — Status scripts read the same runtime artifacts and daemon state the loop writes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
