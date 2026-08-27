---
name: Auto-loop core (auto-loop.sh)
slug: auto-loop-core-auto-loop-sh
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
sources_digest: 9acc0249ddcf7d53dc97c65117d01ec63059f34e1003f3864d7b48ce6de9355a
links:
  - to: budget-spend-accounting
    relation: implements
    description: >-
      Hosts evaluate_budget_gates, record_total_spend, codex_ledger_spend_since,
      _codex_spend_since.
  - to: mcp-config-generation-probe
    relation: uses
    description: Runs jcode-mcp-config.py preflight and jcode-mcp-probe.py before cycles.
  - to: state-snapshot-idle-detection
    relation: uses
    description: >-
      Consumes snapshot DELTA and idle-skip note to decide whether to skip a
      cycle.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop: cycle counter (monotonic across redeploys), budget gates (APP-263), spend accounting from disjoint ccusage + ledger sources, escalation one-shot consumption, idle-skip, engine selection/alternation, MCP config preflight, and window gating. Heavily tested via awk-extracted function fragments.

## Related

- implements [[budget-spend-accounting]] — Hosts evaluate_budget_gates, record_total_spend, codex_ledger_spend_since, _codex_spend_since.
- uses [[mcp-config-generation-probe]] — Runs jcode-mcp-config.py preflight and jcode-mcp-probe.py before cycles.
- uses [[state-snapshot-idle-detection]] — Consumes snapshot DELTA and idle-skip note to decide whether to skip a cycle.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
