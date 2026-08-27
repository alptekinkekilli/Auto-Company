---
name: auto-loop.sh core loop
slug: auto-loop-sh-core-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
sources_digest: 9acc0249ddcf7d53dc97c65117d01ec63059f34e1003f3864d7b48ce6de9355a
links:
  - to: prompt-assembly-contract
    relation: implements
    description: >-
      auto-loop.sh's FULL_PROMPT branches must assemble with embedded guardrail
      text and correct XML section order.
  - to: prompt-transport-contract
    relation: implements
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli pass prompts via STDIN;
      run_jcode_cycle refuses prompts >=126000 bytes.
  - to: set-e-shape-lint
    relation: validates
    description: >-
      test_seteshape_lint.py scans auto-loop.sh for fatal `[ test ] && action`
      shapes.
  - to: tier-ladder-selection
    relation: implements
    description: >-
      apply_tier_ladder() reads TOTAL_DAILY_BUDGET_USD and per-engine daily
      budgets to pick a tier.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration script that runs the daily cycle loop: builds FULL_PROMPT from guardrails, consensus, snapshot, and cycle_orders; applies the daily-budget tier ladder; and transports prompts to engine CLIs (Claude, Codex, jcode) via STDIN or argv. Multiple regression tests pin its invariants because a stray quote or a `set -e`-propagating test list caused production outages (APP-240, APP-263).

## Related

- implements [[prompt-assembly-contract]] — auto-loop.sh's FULL_PROMPT branches must assemble with embedded guardrail text and correct XML section order.
- implements [[prompt-transport-contract]] — run_claude_cycle_cli/run_codex_cycle_cli pass prompts via STDIN; run_jcode_cycle refuses prompts >=126000 bytes.
- validates [[set-e-shape-lint]] — test_seteshape_lint.py scans auto-loop.sh for fatal `[ test ] && action` shapes.
- implements [[tier-ladder-selection]] — apply_tier_ladder() reads TOTAL_DAILY_BUDGET_USD and per-engine daily budgets to pick a tier.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
