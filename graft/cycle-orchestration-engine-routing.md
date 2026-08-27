---
name: Cycle orchestration & engine routing
slug: cycle-orchestration-engine-routing
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 6bd4119d3a03b5716fa89b050999fe63debac1fbae50ba45cf11eb9d36738151
links:
  - to: budget-spend-accounting
    relation: uses
    description: The loop calls evaluate_budget_gates and record_total_spend each cycle.
  - to: mcp-configuration-probe
    relation: uses
    description: >-
      The loop preflights MCP servers via jcode-mcp-probe and generates config
      via jcode-mcp-config.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The core loop (auto-loop.sh) that selects a cycle engine, extracts per-cycle metadata, persists a monotonic cycle counter, applies one-shot escalations, and routes Codex through alternation/fallback. Includes the business-hours window gate, idle-skip mechanism, and discretionary daily cap.

## Related

- uses [[budget-spend-accounting]] — The loop calls evaluate_budget_gates and record_total_spend each cycle.
- uses [[mcp-configuration-probe]] — The loop preflights MCP servers via jcode-mcp-probe and generates config via jcode-mcp-config.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
