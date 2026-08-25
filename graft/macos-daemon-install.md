---
name: macOS daemon install
slug: macos-daemon-install
type: system
sources:
  - path: scripts/macos/install-daemon.sh
    hash: 21f1e9576d7552530f20812f04232c75a2dadb4a7f5e3819045a35dec10037e9
sources_digest: 65656d723a2d52e25953da5035c862691c3124ce59e53f8e71d4827e72e2e064
links:
  - to: loop-lifecycle-monitoring
    relation: produces
    description: The daemon it installs is what status-mac and monitor report on.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Installs/uninstalls the macOS launchd daemon that runs the auto-loop, generating a plist with KeepAlive tied to the pause flag and a 30-second throttle. macOS-only, strict error handling.

## Related

- produces [[loop-lifecycle-monitoring]] — The daemon it installs is what status-mac and monitor report on.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
