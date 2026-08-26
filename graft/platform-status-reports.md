---
name: Platform Status Reports
slug: platform-status-reports
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
    relation: part_of
    description: Status reports and daemon install are part of the loop lifecycle layer.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Platform-specific status reporters emitting the === Section === plus Key=Value format that dashboard/server.py's parse_macos_status_output expects. status-mac.sh checks Guardian (caffeinate), Daemon (launchd), Autostart, Loop, and dumps state/consensus/logs; status-linux.sh is the container adaptation marking sleep guard not_applicable and assuming Coolify restart policy. install-daemon.sh generates the launchd plist with KeepAlive tied to the pause flag.

## Related

- part of [[loop-lifecycle-monitoring]] — Status reports and daemon install are part of the loop lifecycle layer.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
