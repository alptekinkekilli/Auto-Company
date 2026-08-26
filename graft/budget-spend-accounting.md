---
name: Budget & spend accounting
slug: budget-spend-accounting
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
sources_digest: a04fc31ea989f5932fec4aa79082433f470bcbf894e9cba22820c08cccb0c419
links:
  - to: auto-loop-core
    relation: part_of
    description: >-
      Functions evaluate_budget_gates, record_total_spend, _codex_spend_since,
      codex_ledger_spend_since are extracted from auto-loop.sh.
  - to: ops-probe-audit-scripts
    relation: uses
    description: >-
      Discretionary idle detection reads state-snapshot's DELTA: none text;
      spend ledger is discretionary-spend.ndjson.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The spend-measurement and gate logic inside auto-loop.sh: sums Codex spend from two disjoint sources (ccusage CLI sessions + TOTAL_SPEND_LEDGER rows) rather than taking max, is fail-closed on degraded ccusage reads (never lowers a same-period prior observation, latches a hold on first failure), and enforces daily/weekly/5h period gates with rollover independence and run_id dedup.

## Related

- part of [[auto-loop-core]] — Functions evaluate_budget_gates, record_total_spend, _codex_spend_since, codex_ledger_spend_since are extracted from auto-loop.sh.
- uses [[ops-probe-audit-scripts]] — Discretionary idle detection reads state-snapshot's DELTA: none text; spend ledger is discretionary-spend.ndjson.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
