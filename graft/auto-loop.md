---
name: auto_loop
slug: auto-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: a4461971d8736bd0d4fcfaf726ff97173f0f11707e56ebc6b628fd3d33b28aeb
links:
  - to: prompt-transport
    relation: implements
    description: >-
      auto-loop.sh's run_*_cycle_cli functions are the contract that
      test_prompt_transport pins.
  - to: set-e-lint
    relation: validates
    description: >-
      test_seteshape_lint scans auto-loop.sh for the fatal [ test ] && action
      pattern that propagates exit 1.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The core cockpit loop (scripts/core/auto-loop.sh) that assembles the FULL_PROMPT, transports it to engine CLIs, and applies daily-budget tier selection. Prompt assembly must keep XML section order (rules → consensus → snapshot → cycle_orders) and embed guardrail text without stray quotes/backticks/$() that would close the assignment early (a past production outage). Prompt transport: run_claude_cycle_cli and run_codex_cycle_cli pass the prompt via STDIN (codex uses '-' sentinel) to avoid E2BIG from the 131072-byte argv cap; run_jcode_cycle refuses prompts ≥126000 bytes with PROMPT-TOO-LARGE. apply_tier_ladder() selects tiers from daily budgets per engine (APP-263), reading budget-gate variables rather than computing them.

## Related

- implements [[prompt-transport]] — auto-loop.sh's run_*_cycle_cli functions are the contract that test_prompt_transport pins.
- validates [[set-e-lint]] — test_seteshape_lint scans auto-loop.sh for the fatal [ test ] && action pattern that propagates exit 1.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
