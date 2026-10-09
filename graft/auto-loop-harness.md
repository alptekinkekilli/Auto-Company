---
name: Auto-Loop Harness
slug: auto-loop-harness
type: system
sources:
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
sources_digest: effc1772eaeb46b1f07cbaff19f4e4ee4748d43b9719c9ab9cace1be02abe05f
links:
  - to: consensus-pruning
    relation: uses
    description: Invokes consensus-prune.py after ledger-guard.py
  - to: production-mechanism-guard
    relation: validates
    description: auto-loop.sh is a protected surface the guard blocks unplanned writes to
  - to: turn-bloat-escalation
    relation: uses
    description: Invokes turn-bloat-brake.py --record/--feedback
  - to: work-window-brake-watchdog
    relation: uses
    description: Calls work-window.py and wires the watchdog post-cycle
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop (scripts/core/auto-loop.sh) that drives autonomous cycles, with a dense set of fail-closed guards: budget gates (15 behaviors from APP-263), ccusage spend measurement that is fail-closed and never lowers a same-period prior observation, Codex spend summed from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER) rather than max, the work-window brake, consensus pruning, and the turn-bloat brake. Includes the _window_active() business-hours gate with octal-trap handling and fail-open behavior so a typo never parks the company.

## Related

- uses [[consensus-pruning]] — Invokes consensus-prune.py after ledger-guard.py
- validates [[production-mechanism-guard]] — auto-loop.sh is a protected surface the guard blocks unplanned writes to
- uses [[turn-bloat-escalation]] — Invokes turn-bloat-brake.py --record/--feedback
- uses [[work-window-brake-watchdog]] — Calls work-window.py and wires the watchdog post-cycle
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
