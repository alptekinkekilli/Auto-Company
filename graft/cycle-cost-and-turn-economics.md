---
name: Cycle Cost and Turn Economics
slug: cycle-cost-and-turn-economics
type: system
sources:
  - path: scripts/ops/cost-audit.py
    hash: 5364d89f8098cbb2fd8e51d0ba2c3c79a26df3dd6b99abb97cfa228af0cb8867
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
  - path: tests/test_cost_audit_tool_surface.py
    hash: 801b92c715ca95cef9c34ab863f87fa443c8abcc65ba03237a934f5aed78121a
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
sources_digest: 7ab230a9de08e9cc4f607a3437fec40e7eeb7f9e23259fb617c393a9459e28e4
links:
  - to: auto-loop-harness-brakes-and-guards
    relation: produces
    description: >-
      Cost and turn measurements feed the budget gates and turn-bloat-brake
      verdicts
  - to: budget-gates-and-spend-accounting
    relation: uses
    description: Cost figures feed the ccusage/ledger spend accounting
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
  - symbol: ts_of
    kind: function
    at: 'scripts/ops/turn-audit.py:L74-L78'
  - symbol: scan
    kind: function
    at: 'scripts/ops/turn-audit.py:L81-L112'
  - symbol: floor_usd
    kind: function
    at: 'scripts/ops/turn-audit.py:L115-L118'
  - symbol: summary_line
    kind: function
    at: 'scripts/ops/turn-audit.py:L121-L139'
  - symbol: main
    kind: function
    at: 'scripts/ops/turn-audit.py:L142-L155'
  - symbol: is_web
    kind: function
    at: 'scripts/ops/web-research-cost.py:L43-L44'
  - symbol: analyse
    kind: function
    at: 'scripts/ops/web-research-cost.py:L47-L76'
  - symbol: main
    kind: function
    at: 'scripts/ops/web-research-cost.py:L79-L161'
  - symbol: ok
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L24-L25'
  - symbol: 'no'
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L28-L31'
---
<!-- context:generated:start -->
## Summary

The per-cycle cost and turn-economics measurement layer: engine-usage-cost.py prices token streams (with a --model-hint that must never override an actual completed model), turn-audit.py measures per-session turn count/context growth/cache traffic/cost floor, web-research-cost.py corrects the naive 'fetch costs once' assumption by scoring residual cost as output_tokens × turns_after × cache-read rate, and cost-audit.py computes the advertised tool surface subtracting JCODE_TOOLS_DENY-hidden tools. These feed the budget gates and bloat brakes.

## Related

- produces [[auto-loop-harness-brakes-and-guards]] — Cost and turn measurements feed the budget gates and turn-bloat-brake verdicts
- uses [[budget-gates-and-spend-accounting]] — Cost figures feed the ccusage/ledger spend accounting
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
