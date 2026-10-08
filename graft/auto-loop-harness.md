---
name: Auto-Loop Harness
slug: auto-loop-harness
type: system
sources:
  - path: scripts/wsl/install-wsl-daemon.sh
    hash: 2b1d8ba1d5064ade6c138f43bd573d49b659b8bf9f5729d3d339a2ace4ee919b
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 82fd9dfa80c4f0c916c506e6a44db71dbfd6ee1c0421bcedf8d255b77c3bfd7e
  - path: tests/test_auto_loop_ledger_guard.sh
    hash: 707a207723f0b5c371c39d0fbc5a14170b4c74bb9c893f550186797aebcf440f
  - path: tests/test_auto_loop_work_window.sh
    hash: 7bb4ebdcaef7c71820540195fab59c8c657ff11f525429105bb0376a30405369
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
sources_digest: 22cd2a480ea66971e05179ebb8fcf9f58086dddbbbeda1256b50b7156423e5b0
links:
  - to: cycle-economics-auditing
    relation: uses
    description: The harness's budget gates consume ccusage and ledger spend figures.
  - to: fail-closed-operational-brakes
    relation: uses
    description: >-
      The harness invokes work-window, turn-bloat-brake, ledger-guard, and
      consensus-prune, gating idle-skip and cycle behavior on their exit codes.
  - to: prod-mechanism-guard
    relation: validates
    description: >-
      auto-loop.sh is a protected suffix; prod-mechanism-guard.py blocks
      unplanned edits to it.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration script scripts/core/auto-loop.sh that drives autonomous cycles: selects the cycle engine, evaluates budget gates (15 behaviors from APP-263), enforces the active-window business-hours gate, records spend from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER, summed not maxed), and wires in the operational brakes and guards. It is a protected production surface (guarded by prod-mechanism-guard.py) and is heavily tested via awk-extracted function harnesses.

## Related

- uses [[cycle-economics-auditing]] — The harness's budget gates consume ccusage and ledger spend figures.
- uses [[fail-closed-operational-brakes]] — The harness invokes work-window, turn-bloat-brake, ledger-guard, and consensus-prune, gating idle-skip and cycle behavior on their exit codes.
- validates [[prod-mechanism-guard]] — auto-loop.sh is a protected suffix; prod-mechanism-guard.py blocks unplanned edits to it.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
