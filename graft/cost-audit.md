---
name: cost-audit
slug: cost-audit
type: file
sources:
  - path: scripts/ops/cost-audit.py
    hash: f861b3352eb593e372a5a81bdaa068411ec3c7aa179e78df814b68dafffd08f7
sources_digest: cf9d44fdc47a642ca0c0cedff032a3bc13f195d548c751529bf2568e013c8b6a
links: []
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

Deterministic daily cost-audit writing markdown report to memories/cost-audit.md before the Opportunity Analyst runs. Parses spend-total.log, auto-loop.log telemetry/cost/turn-audit/timeout lines, jcode logs, mcp-schema-cache. Reports on previous completed UTC day (runs 04:30 before LOOP_ACTIVE_WINDOW_UTC opens, so 'today' would be zero). Company-fixable findings routed to directive Ops hygiene; infra raised as OPREQs. Never estimates, judges, or writes outside its own file.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
