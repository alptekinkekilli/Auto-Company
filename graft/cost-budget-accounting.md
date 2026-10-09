---
name: Cost & budget accounting
slug: cost-budget-accounting
type: system
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
  - path: scripts/ops/cost-audit.py
    hash: 5364d89f8098cbb2fd8e51d0ba2c3c79a26df3dd6b99abb97cfa228af0cb8867
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
sources_digest: 6fb629ee9880123491a0128cf07e0e4887169443c294bae98d7fccfe913ecd86
links:
  - to: final-text-extraction-from-event-streams
    relation: uses
    description: engine-usage-cost parses the same jcode --ndjson format.
  - to: operator-notification-routing
    relation: uses
    description: >-
      budget-calibration-report reads operator-usage.json pushed by
      operator-usage-report.sh for the operator-impact section.
generator:
  version: 1
covers:
  - symbol: _n
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L66-L69'
  - symbol: cost_for
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L72-L110'
  - symbol: main
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L113-L191'
  - symbol: split_by_cutover
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L72-L76'
  - symbol: pct
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L79-L84'
  - symbol: load_claude
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L87-L102'
  - symbol: load_codex
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L105-L138'
  - symbol: sliding
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L141-L157'
  - symbol: daily_buckets
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L160-L166'
  - symbol: stats_line
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L169-L173'
  - symbol: main
    kind: function
    at: 'scripts/ops/budget-calibration-report.py:L176-L289'
  - symbol: utc_day
    kind: function
    at: 'scripts/ops/cost-audit.py:L42-L43'
  - symbol: read_ledger
    kind: function
    at: 'scripts/ops/cost-audit.py:L46-L67'
  - symbol: read_loop_log
    kind: function
    at: 'scripts/ops/cost-audit.py:L70-L111'
  - symbol: read_jcode_log
    kind: function
    at: 'scripts/ops/cost-audit.py:L114-L131'
  - symbol: read_tool_inventory
    kind: function
    at: 'scripts/ops/cost-audit.py:L134-L141'
  - symbol: read_disabled_tools
    kind: function
    at: 'scripts/ops/cost-audit.py:L144-L171'
  - symbol: fmt_money
    kind: function
    at: 'scripts/ops/cost-audit.py:L174-L175'
  - symbol: build_report
    kind: function
    at: 'scripts/ops/cost-audit.py:L178-L339'
  - symbol: main
    kind: function
    at: 'scripts/ops/cost-audit.py:L342-L360'
---
<!-- context:generated:start -->
## Summary

Converts token usage into notional USD and audits spend. engine-usage-cost applies a hardcoded PRICES table with uniform cache multipliers, prices unknown models at 5x the most expensive known row (flagged estimated:true) to avoid silent zero-cost budget gates, and sums ALL tokens events (not just done.usage, which undercounts multi-tool cycles). cost-audit builds a deterministic daily report from on-disk logs only, reporting on the prior day to avoid empty current-day data and separating company-fixable findings from infra issues that must go to OPREQ. budget-calibration-report splits pre/post data at CUTOVER_EPOCH (2026-08-10) to avoid blending two different pause-gate policies.

## Related

- uses [[final-text-extraction-from-event-streams]] — engine-usage-cost parses the same jcode --ndjson format.
- uses [[operator-notification-routing]] — budget-calibration-report reads operator-usage.json pushed by operator-usage-report.sh for the operator-impact section.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
