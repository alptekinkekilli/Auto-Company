---
name: budget-calibration-report
slug: budget-calibration-report
type: file
sources:
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
sources_digest: 8f3b06db4c4315c406bae1790bbfc4b71680341be802e154cbc2f765c8b9fcfb
links: []
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

APP-263 budget calibration report from operational logs over configurable window (14 days). Reads Claude spend from spend-total.log, Codex via ccusage (excluding analyst), parses auto-loop.log for gate blocks/pauses. CUTOVER_EPOCH (2026-08-10) splits pre/post data to avoid blending two policies (per-engine 5-hour pause gate retired). Never modifies thresholds, only reports.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
