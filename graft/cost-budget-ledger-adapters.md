---
name: Cost & Budget Ledger Adapters
slug: cost-budget-ledger-adapters
type: system
sources:
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
  - path: scripts/ops/cost-audit.py
    hash: f861b3352eb593e372a5a81bdaa068411ec3c7aa179e78df814b68dafffd08f7
sources_digest: d8409f0423cddadfa37b66cf1c0637a59912b33c8467b041650ebe655f2facb2
links:
  - to: operator-escalation-notification
    relation: uses
    description: >-
      cost-audit.py routes company-fixable findings to the directive's Ops
      hygiene block and raises infra findings as OPREQs, which
      operator_request_notify.py consumes.
  - to: telegram-notification-channel
    relation: uses
    description: >-
      budget-calibration-report.py and cost-audit.py rely on telegram-notify.sh
      for alerts.
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

Converts token-usage and spend data into USD costs and budget reports for the APP-263 ledger. engine-usage-cost.py adapts jcode's token-only output (summing all tokens events, not just done.usage) into notional USD via a hardcoded PRICES table with conservative unknown-model pricing (5x most-expensive, estimated:true, STRICT=1 exits 3). budget-calibration-report.py and cost-audit.py parse on-disk logs to produce spend percentiles and markdown reports, deliberately reporting on the previous completed UTC day and never estimating or writing outside their own output.

## Related

- uses [[operator-escalation-notification]] — cost-audit.py routes company-fixable findings to the directive's Ops hygiene block and raises infra findings as OPREQs, which operator_request_notify.py consumes.
- uses [[telegram-notification-channel]] — budget-calibration-report.py and cost-audit.py rely on telegram-notify.sh for alerts.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
