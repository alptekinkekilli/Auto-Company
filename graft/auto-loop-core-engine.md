---
name: Auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
sources_digest: 0b7277763f7379a71ac05648532b143d79d145d71b19ad3b17f02fff588efdc0
links:
  - to: budget-spend-accounting
    relation: uses
    description: >-
      calls evaluate_budget_gates, record_total_spend, apply_tier_ladder,
      _codex_spend_since
  - to: operator-escalation
    relation: uses
    description: apply_cycle_escalation consumes one-shot escalation from runtime.env
  - to: prod-mechanism-guard
    relation: validates
    description: is a protected path blocked by the PreToolUse hook
  - to: prompt-transport-contract
    relation: implements
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle must pass prompts
      via STDIN and refuse oversized prompts
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop that runs cycles, applies budget gates, tier ladders, escalation, idle-skip, and prompt assembly. It is the single most protected surface in the repo (guarded by prod-mechanism-guard).

## Related

- uses [[budget-spend-accounting]] — calls evaluate_budget_gates, record_total_spend, apply_tier_ladder, _codex_spend_since
- uses [[operator-escalation]] — apply_cycle_escalation consumes one-shot escalation from runtime.env
- validates [[prod-mechanism-guard]] — is a protected path blocked by the PreToolUse hook
- implements [[prompt-transport-contract]] — run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle must pass prompts via STDIN and refuse oversized prompts
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
