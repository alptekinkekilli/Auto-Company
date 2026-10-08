---
name: Auto-loop harness & budget governance
slug: auto-loop-harness-budget-governance
type: system
sources:
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
sources_digest: 21e34877363b1805e6f80d09ab7da187ee975237d42c0d8a55e43a221b9084dd
links:
  - to: operational-guard-tripwires
    relation: part_of
    description: >-
      The budget gates and spend measurement live in auto-loop.sh alongside the
      work-window and ledger guards.
  - to: work-window-bloat-brakes
    relation: uses
    description: >-
      Budget gates are the money backstop against a stuck-open work window;
      spend measurement feeds the bloat brake's cost threshold.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The core autonomous loop (scripts/core/auto-loop.sh) and its budget/spend governance: ccusage-based spend measurement that is fail-closed (degraded reads never lower a same-period prior observation), budget gates per engine with rollover independence, and spend summed from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER) rather than maxed. Enforces fail-closed semantics where any unmeasurable spend latches a hold and returns NA, never 0.

## Related

- part of [[operational-guard-tripwires]] — The budget gates and spend measurement live in auto-loop.sh alongside the work-window and ledger guards.
- uses [[work-window-bloat-brakes]] — Budget gates are the money backstop against a stuck-open work window; spend measurement feeds the bloat brake's cost threshold.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
