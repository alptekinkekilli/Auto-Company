---
name: Auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
sources_digest: 0b7277763f7379a71ac05648532b143d79d145d71b19ad3b17f02fff588efdc0
links:
  - to: budget-and-spend-accounting
    relation: uses
    description: >-
      evaluate_budget_gates, record_total_spend, apply_tier_ladder, and
      spend-since functions live here and are extracted by tests.
  - to: prod-mechanism-guard
    relation: validates
    description: >-
      auto-loop.sh is a protected path that the PreToolUse hook blocks edits to
      without an approval marker.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop in scripts/core/auto-loop.sh that drives cycles, budget gates, tier ladders, escalation, idle-skip, prompt assembly, and engine routing. It is the most protected surface in the repo and the target of most regression tests.

## Related

- uses [[budget-and-spend-accounting]] — evaluate_budget_gates, record_total_spend, apply_tier_ladder, and spend-since functions live here and are extracted by tests.
- validates [[prod-mechanism-guard]] — auto-loop.sh is a protected path that the PreToolUse hook blocks edits to without an approval marker.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
