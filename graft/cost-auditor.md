---
name: Cost auditor
slug: cost-auditor
type: system
sources:
  - path: scripts/ops/cost-audit.py
    hash: 5364d89f8098cbb2fd8e51d0ba2c3c79a26df3dd6b99abb97cfa228af0cb8867
sources_digest: 465748869edd1e50cef755b40addaae36956a2c2727741754f1b949ddc033fff
links:
  - to: budget-calibration-report
    relation: uses
    description: Both read spend-total.log and auto-loop.log for spend/gate data.
  - to: mcp-config-generation-boot-probe
    relation: uses
    description: >-
      Reads the MCP schema cache and denylist to compute advertised-vs-called
      tool surface.
generator:
  version: 1
covers:
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

Deterministic daily cost auditor running before the Opportunity Analyst, writing a Markdown report from on-disk logs only — never model estimates. Reports on the prior completed UTC day (04:30 cron before active window), subtracts loop-hidden tools to avoid false trim findings, flags phantom costs from uncalibrated model estimates, and separates company-fixable findings (memory bloat, chatty cycles) from infra issues that must go to OPREQ.

## Related

- uses [[budget-calibration-report]] — Both read spend-total.log and auto-loop.log for spend/gate data.
- uses [[mcp-config-generation-boot-probe]] — Reads the MCP schema cache and denylist to compute advertised-vs-called tool surface.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
