---
name: Budget calibration & cost audit
slug: budget-calibration-cost-audit
type: system
sources:
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
  - path: scripts/ops/cost-audit.py
    hash: 5364d89f8098cbb2fd8e51d0ba2c3c79a26df3dd6b99abb97cfa228af0cb8867
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
sources_digest: 34fed35fedd56e2ab8fb7dcd433d69ebb86a2746abba6f95b31acc503753673f
links:
  - to: opportunity-analyst-cron
    relation: uses
    description: >-
      cost-audit.py runs before the Opportunity Analyst and its report feeds the
      analyst's context.
generator:
  version: 1
covers:
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

Deterministic cost reporting from on-disk logs only, never model estimates. budget-calibration-report.py summarizes spend percentiles and gate-block counts over a window, splitting pre/post data at CUTOVER_EPOCH (2026-08-10) when the per-engine 5-hour pause gate was retired, and approximating 5-hour peaks via hourly sliding windows because exact plan anchors aren't retained. cost-audit.py writes memories/cost-audit.md before the Opportunity Analyst, reporting on the previous completed UTC day (04:30 cron before active window), subtracting loop-hidden tools to avoid false trim findings, and flagging phantom costs from uncalibrated model estimates. operator-usage-report.sh pushes the operator's ccusage active-block spend into the container, with file mtime as the freshness signal so a stopped reporter degrades gracefully.

## Related

- uses [[opportunity-analyst-cron]] — cost-audit.py runs before the Opportunity Analyst and its report feeds the analyst's context.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
