---
name: cost & budget telemetry
slug: cost-budget-telemetry
type: system
sources:
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
  - path: scripts/ops/cost-audit.py
    hash: f861b3352eb593e372a5a81bdaa068411ec3c7aa179e78df814b68dafffd08f7
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
sources_digest: fb34fb3c3c53188aba9ed26a7b2a2ad113854edc65a18af8d7b9f598fcc44b58
links:
  - to: operator-escalation-gate
    relation: produces
    description: >-
      cost-audit.md and operator-usage.json are the measured inputs the
      escalation gate and analyst interpret.
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

Deterministic cost/budget reporting from on-disk logs, never estimating or judging. cost-audit.py writes a six-section markdown report to memories/cost-audit.md before the Opportunity Analyst, reporting on the previous completed UTC day (a 'today' figure would always be zero at 04:30 UTC) and routing findings to directives vs OPREQs. budget-calibration-report.py splits pre/post data at CUTOVER_EPOCH (2026-08-10) to avoid blending two different 5-hour pause-gate policies. operator-usage-report.sh pushes the operator's ccusage block into the container, with file mtime as the freshness signal so a stopped reporter degrades gracefully.

## Related

- produces [[operator-escalation-gate]] — cost-audit.md and operator-usage.json are the measured inputs the escalation gate and analyst interpret.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
