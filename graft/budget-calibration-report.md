---
name: Budget calibration report
slug: budget-calibration-report
type: system
sources:
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
sources_digest: 102f2f19e353c8cfb04d1b827e2ce34860484612409b4179f54f863e99f69c19
links:
  - to: engine-usage-cost-adapter
    relation: uses
    description: >-
      Reads spend from spend-total.log and ccusage; operator-usage-report.sh
      pushes the operator's active-block spend into the container for
      calibration.
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
---
<!-- context:generated:start -->
## Summary

Generates an APP-263 budget calibration report from operational logs, splitting pre/post data at CUTOVER_EPOCH (2026-08-10) when the per-engine 5-hour pause gate was retired, approximating 5-hour peaks via hourly sliding windows, and reporting gate-block tallies and operator-impact signals. Never modifies thresholds — it only reports.

## Related

- uses [[engine-usage-cost-adapter]] — Reads spend from spend-total.log and ccusage; operator-usage-report.sh pushes the operator's active-block spend into the container for calibration.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
