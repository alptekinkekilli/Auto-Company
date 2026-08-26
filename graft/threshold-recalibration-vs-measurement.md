---
name: Threshold Recalibration vs Measurement
slug: threshold-recalibration-vs-measurement
type: concept
sources:
  - path: scripts/ops/bloat-trend.py
    hash: f74441749dee8335f3eb7b9fa4626fcde6b9903cf0006019a261e8c35115fe26
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
  - path: scripts/ops/cost-audit.py
    hash: f861b3352eb593e372a5a81bdaa068411ec3c7aa179e78df814b68dafffd08f7
sources_digest: a7de95e6ae47c5ade03f1de2a4f7e5613041ab1419ddd9d9f4b164786859b1cd
links:
  - to: cost-budget-ledger-adapters
    relation: implements
    description: These scripts embody the recalibration-vs-measurement principle.
generator:
  version: 1
covers:
  - symbol: ingest
    kind: function
    at: 'scripts/ops/bloat-trend.py:L54-L97'
  - symbol: is_bloated
    kind: function
    at: 'scripts/ops/bloat-trend.py:L109-L110'
  - symbol: summarise
    kind: function
    at: 'scripts/ops/bloat-trend.py:L113-L126'
  - symbol: pct
    kind: function
    at: 'scripts/ops/bloat-trend.py:L117-L118'
  - symbol: notify
    kind: function
    at: 'scripts/ops/bloat-trend.py:L129-L142'
  - symbol: fmt
    kind: function
    at: 'scripts/ops/bloat-trend.py:L145-L155'
  - symbol: d
    kind: function
    at: 'scripts/ops/bloat-trend.py:L146-L151'
  - symbol: main
    kind: function
    at: 'scripts/ops/bloat-trend.py:L158-L237'
  - symbol: hits_target
    kind: function
    at: 'scripts/ops/bloat-trend.py:L185-L187'
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
  - symbol: fmt_money
    kind: function
    at: 'scripts/ops/cost-audit.py:L144-L145'
  - symbol: build_report
    kind: function
    at: 'scripts/ops/cost-audit.py:L148-L303'
  - symbol: main
    kind: function
    at: 'scripts/ops/cost-audit.py:L306-L324'
---
<!-- context:generated:start -->
## Summary

A design principle that stored verdicts are recomputed from raw numbers using current thresholds, so comparisons measure cycles, not the ruler. bloat-trend.py recomputes stored verdicts because thresholds changed on 2026-08-02; budget-calibration-report.py splits pre/post data at CUTOVER_EPOCH (2026-08-10) to avoid blending two different pause-gate policies; cost-audit.py reports on the previous completed UTC day because it runs before the daily window opens.

## Related

- implements [[cost-budget-ledger-adapters]] — These scripts embody the recalibration-vs-measurement principle.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
