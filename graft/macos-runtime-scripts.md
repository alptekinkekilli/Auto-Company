---
name: macos-runtime-scripts
slug: macos-runtime-scripts
type: system
sources:
  - path: scripts/macos/install-daemon.sh
    hash: 21f1e9576d7552530f20812f04232c75a2dadb4a7f5e3819045a35dec10037e9
  - path: scripts/macos/status-mac.sh
    hash: ba8bc08141ca80245bea6ccb35984221942d6a855ce856e5a492a38c4c151418
sources_digest: 4507048c9a0c0ed781087049d96ec7fdda432147086e012e904d8fcd0cd75a59
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

macOS launchd daemon install/uninstall and status reporting. install-daemon.sh generates plist dynamically, KeepAlive tied to .auto-loop-paused so daemon stays alive unless that file exists, 30s throttle. status-mac.sh checks Guardian (caffeinate), Daemon, Autostart, Loop, then dumps state/consensus/logs in Key=Value format for the dashboard.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
