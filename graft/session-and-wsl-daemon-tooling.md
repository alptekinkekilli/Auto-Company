---
name: Session and WSL daemon tooling
slug: session-and-wsl-daemon-tooling
type: system
sources:
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
  - path: scripts/wsl/install-wsl-daemon.sh
    hash: 2b1d8ba1d5064ade6c138f43bd573d49b659b8bf9f5729d3d339a2ace4ee919b
  - path: scripts/wsl/uninstall-wsl-daemon.sh
    hash: 9a3367f7cbb052a83488d12ed50a81a8d09ff2a5c04ac7620b213b9f052936e3
  - path: scripts/wsl/wsl-daemon-status.sh
    hash: 55fb93df7f080f48a322d005e6b1f76ec2de1c5283de176883b0644d69f39a6a
sources_digest: e7fec27e384fae3e60130a562ad01c7a355dafa856181c5fa53f51751d165246
links:
  - to: auto-loop-core-engine
    relation: uses
    description: The WSL daemon runs auto-loop.sh from the project root.
generator:
  version: 1
covers:
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L19-L23'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L26-L63'
---
<!-- context:generated:start -->
## Summary

session-brief.py (SessionStart hook injecting measured git state, never blocking, never writing secrets) and the WSL systemd daemon install/uninstall/status scripts for running auto-loop.sh as a per-user service with Restart=always.

## Related

- uses [[auto-loop-core-engine]] — The WSL daemon runs auto-loop.sh from the project root.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
