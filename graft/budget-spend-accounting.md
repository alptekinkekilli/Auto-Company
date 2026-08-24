---
name: Budget & Spend Accounting
slug: budget-spend-accounting
type: system
sources:
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 277061fac132ba9be3f24fea9cd7d06fcbdd82414ad6299ebbce5aff73075e2a
links:
  - to: auto-loop-core
    relation: part_of
    description: >-
      Functions like evaluate_budget_gates, record_total_spend,
      apply_tier_ladder are extracted from auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The spend-measurement and budget-gate machinery: ccusage reads, codex ledger summation, record_total_spend, and the 15 APP-263 budget gates. Enforces fail-closed behavior where degraded reads never lower a same-period prior observation and never overwrite the cache.

## Related

- part of [[auto-loop-core]] — Functions like evaluate_budget_gates, record_total_spend, apply_tier_ladder are extracted from auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
