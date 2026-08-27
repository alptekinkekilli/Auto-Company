---
name: Cost audit
slug: cost-audit
type: system
sources:
  - path: scripts/ops/budget-calibration-report.py
    hash: 4773ab252d5a928ff27a3bb15b9df63d086258a96e76d0d679ebeba49985be21
  - path: scripts/ops/cost-audit.py
    hash: f861b3352eb593e372a5a81bdaa068411ec3c7aa179e78df814b68dafffd08f7
sources_digest: cd839802af03e56c29d676248481f3c39fafaef219c9247cefff4f251b644c6d
links:
  - to: engine-usage-cost-adapter
    relation: uses
    description: Consumes per-model cost figures for the report.
  - to: mcp-config-generation-and-probe
    relation: uses
    description: Reads mcp-schema-cache.json for advertised MCP tool surfaces.
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

Deterministic daily cost-audit that parses on-disk logs and writes a markdown report to memories/cost-audit.md, running before the Opportunity Analyst so the agent interprets measured numbers rather than re-deriving them. Reports on the previous completed UTC day (it runs at 04:30 before the daily window opens), classifies findings as company-fixable (routed to the directive's ## Ops hygiene block) versus infra (raised as OPREQs, never directives), and distinguishes calibrated costs from 'phantom' estimated costs.

## Related

- uses [[engine-usage-cost-adapter]] — Consumes per-model cost figures for the report.
- uses [[mcp-config-generation-and-probe]] — Reads mcp-schema-cache.json for advertised MCP tool surfaces.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
