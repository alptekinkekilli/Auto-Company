---
name: Auto-Loop Harness
slug: auto-loop-harness
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: scripts/wsl/install-wsl-daemon.sh
    hash: 2b1d8ba1d5064ade6c138f43bd573d49b659b8bf9f5729d3d339a2ace4ee919b
  - path: scripts/wsl/uninstall-wsl-daemon.sh
    hash: 9a3367f7cbb052a83488d12ed50a81a8d09ff2a5c04ac7620b213b9f052936e3
  - path: scripts/wsl/wsl-daemon-status.sh
    hash: 55fb93df7f080f48a322d005e6b1f76ec2de1c5283de176883b0644d69f39a6a
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
sources_digest: aeaabb5f66acc8eeb708286b1e65e0d718404da3b78118e03cff6a924feb2be7
links:
  - to: cycle-escalation-brakes
    relation: uses
    description: >-
      The loop invokes work-window.py, turn-bloat-brake.py, and the watchdog as
      pre/post-cycle hooks.
  - to: production-mechanism-guard
    relation: validates
    description: >-
      auto-loop.sh is a protected surface; prod-mechanism-guard.py blocks
      unplanned edits to it unless a fresh approval marker exists.
  - to: state-snapshot-consensus
    relation: uses
    description: >-
      The loop calls consensus-prune.py after ledger-guard.py and gates it on
      cycle_failed_reason being empty.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The core autonomous loop (scripts/core/auto-loop.sh) that drives cycles, plus its WSL systemd daemon packaging. It integrates the budget gates, work-window brake, consensus-prune, ledger-guard, and turn-bloat-brake as hooks, with strict wiring order (e.g. _window_active must run before select_cycle_engine and before the loop_count increment so off-hours ticks don't burn cycle numbers). Budget gates (APP-263) cover engine-specific gates, rollover independence, daily/weekly resets, duplicate run_id dedup, analyst session exclusion, and stale-fallback behavior; ccusage measurement is fail-closed so degraded reads never lower a same-period prior observation, and Codex spend is summed from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER) rather than maxed. The WSL scripts install/uninstall/status a per-user systemd service running auto-loop.sh with Restart=always.

## Related

- uses [[cycle-escalation-brakes]] — The loop invokes work-window.py, turn-bloat-brake.py, and the watchdog as pre/post-cycle hooks.
- validates [[production-mechanism-guard]] — auto-loop.sh is a protected surface; prod-mechanism-guard.py blocks unplanned edits to it unless a fresh approval marker exists.
- uses [[state-snapshot-consensus]] — The loop calls consensus-prune.py after ledger-guard.py and gates it on cycle_failed_reason being empty.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
