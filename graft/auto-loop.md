---
name: auto-loop
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
  - to: prompt-transport-contract
    relation: implements
    description: >-
      auto-loop.sh's run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle
      must honor the STDIN/argv transport contract.
  - to: set-e-shape-lint
    relation: validates
    description: 'auto-loop.sh is linted for the fatal [ test ] && action set -e pattern.'
  - to: turn-economy
    relation: uses
    description: >-
      The loop's turn-feedback slot feeds the turn-economy policy audited by
      turn-audit.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The cockpit's core orchestration loop: assembles the FULL_PROMPT from guardrail text, consensus, snapshot, and cycle counters; transports the prompt to engine CLIs (Claude via STDIN, Codex via '-' sentinel, jcode via argv with a 126000-byte PROMPT-TOO-LARGE refusal); and selects daily-budget tiers via apply_tier_ladder(). Guardrail assembly is fragile — a stray double quote previously closed the assignment early and caused a production outage that bash -n could not detect.

## Related

- implements [[prompt-transport-contract]] — auto-loop.sh's run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle must honor the STDIN/argv transport contract.
- validates [[set-e-shape-lint]] — auto-loop.sh is linted for the fatal [ test ] && action set -e pattern.
- uses [[turn-economy]] — The loop's turn-feedback slot feeds the turn-economy policy audited by turn-audit.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
