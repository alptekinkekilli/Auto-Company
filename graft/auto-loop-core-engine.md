---
name: auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
sources_digest: 903c7dcb6c440915b2bed1d5c8d80f286a371c253704e4713d742468a8760e27
links:
  - to: cycle-counter-persistence
    relation: implements
    description: >-
      auto-loop.sh owns the CYCLE_COUNTER_FILE init and persist lines that the
      counter tests extract and drive.
  - to: escalation-one-shot
    relation: implements
    description: >-
      apply_cycle_escalation/_consume_escalation implement the
      consume-exactly-once operator escalation.
  - to: idle-skip-mechanism
    relation: implements
    description: >-
      _idle_skip_due and the skip branch implement idle detection and the
      never-skip-first-cycle rule.
  - to: mcp-config-sync
    relation: depends_on
    description: >-
      auto-loop.sh's JCODE_MCP_CONFIG_REQUIRED preflight list must agree with
      the manifest and generated config.
  - to: prompt-transport-contract
    relation: implements
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle define how
      prompts reach engine CLIs (STDIN vs argv).
  - to: set-e-shape-lint
    relation: validates
    description: >-
      test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action
      pattern that caused APP-240.
  - to: tier-ladder-budgeting
    relation: implements
    description: apply_tier_ladder() selects engine tiers from daily budget spend.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration loop (scripts/core/auto-loop.sh) that drives per-cycle engine selection (claude/jcode/codex), prompt assembly, cycle-counter persistence, escalation, tier-ladder budgeting, idle-skip, and metadata extraction. It is the highest-risk surface in the repo: a stray quote, a set -e shape, or a counter reset can crash the whole container, which is why an unusually large share of the test suite exists to pin its behavior.

## Related

- implements [[cycle-counter-persistence]] — auto-loop.sh owns the CYCLE_COUNTER_FILE init and persist lines that the counter tests extract and drive.
- implements [[escalation-one-shot]] — apply_cycle_escalation/_consume_escalation implement the consume-exactly-once operator escalation.
- implements [[idle-skip-mechanism]] — _idle_skip_due and the skip branch implement idle detection and the never-skip-first-cycle rule.
- depends on [[mcp-config-sync]] — auto-loop.sh's JCODE_MCP_CONFIG_REQUIRED preflight list must agree with the manifest and generated config.
- implements [[prompt-transport-contract]] — run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle define how prompts reach engine CLIs (STDIN vs argv).
- validates [[set-e-shape-lint]] — test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action pattern that caused APP-240.
- implements [[tier-ladder-budgeting]] — apply_tier_ladder() selects engine tiers from daily budget spend.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
