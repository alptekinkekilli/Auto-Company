---
name: fail-closed measurement & spend accounting
slug: fail-closed-measurement-spend-accounting
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
sources_digest: 91e1f62002eebcbcec085802a5e9438052acfb76ab147baca80859029f7ef0e4
links:
  - to: auto-loop-core
    relation: implements
    description: 'Encoded in evaluate_budget_gates, _codex_spend_since, record_total_spend.'
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A cross-cutting invariant: ccusage and spend measurements are fail-closed (degraded reads never lower a same-period prior observation, first-ever failure latches a hold and returns NA not 0), spend is summed from two disjoint sources (ccusage + TOTAL_SPEND_LEDGER) rather than maxed, and budget gates are deterministic via BUDGET_NOW_OVERRIDE.

## Related

- implements [[auto-loop-core]] — Encoded in evaluate_budget_gates, _codex_spend_since, record_total_spend.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
