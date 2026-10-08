---
name: macOS launchd daemon management
slug: macos-launchd-daemon-management
type: system
sources:
  - path: scripts/macos/install-daemon.sh
    hash: 21f1e9576d7552530f20812f04232c75a2dadb4a7f5e3819045a35dec10037e9
  - path: scripts/macos/status-mac.sh
    hash: ba8bc08141ca80245bea6ccb35984221942d6a855ce856e5a492a38c4c151418
sources_digest: 4507048c9a0c0ed781087049d96ec7fdda432147086e012e904d8fcd0cd75a59
links:
  - to: loop-lifecycle-monitoring-core-shell
    relation: uses
    description: >-
      stop-loop.sh --pause-daemon/--resume-daemon manage the same launchd daemon
      and .auto-loop-paused flag.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

macOS-specific lifecycle: install-daemon.sh generates a plist dynamically and loads it into ~/Library/LaunchAgents/, with KeepAlive tied to the .auto-loop-paused flag so the daemon stays alive unless that file exists, a 30-second throttle to prevent rapid restarts, and a custom PATH including the engine's directory. status-mac.sh reports Guardian (caffeinate), Daemon, Autostart, Loop, state file, consensus, and recent log as key-value pairs for the dashboard.

## Related

- uses [[loop-lifecycle-monitoring-core-shell]] — stop-loop.sh --pause-daemon/--resume-daemon manage the same launchd daemon and .auto-loop-paused flag.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
