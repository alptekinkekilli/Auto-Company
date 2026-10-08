---
name: auto-loop core engine
slug: auto-loop-core-engine
type: system
sources:
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
  - path: tests/test_mcp_config_manifest_sync.sh
    hash: 372a198973bc97e73dd00c1acafe2fe458887504be2f5ef9849242d6549c1112
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: df7ea88d533647418cf9e1eaaa0ddf47f1f75600984d272b222a600a6f87b2c4
links:
  - to: cycle-counter-persistence
    relation: implements
    description: >-
      auto-loop.sh's seed block and persist line define the monotonic cycle
      counter that test_cycle_counter.sh extracts and drives
  - to: cycle-metadata-extraction
    relation: implements
    description: >-
      extract_cycle_metadata() parses engine output into
      CYCLE_TYPE/SUBTYPE/RESULT_TEXT, tested by test_cycle_metadata.sh
  - to: escalation-one-shot-logic
    relation: implements
    description: >-
      apply_cycle_escalation/_consume_escalation/_directive_is_pending implement
      the APP-238 one-shot operator escalation
  - to: idle-skip-mechanism
    relation: implements
    description: >-
      _idle_skip_due and the skip branch implement idle detection and
      consensus-note wiring
  - to: prompt-assembly-contract
    relation: implements
    description: >-
      FULL_PROMPT assignments must assemble with guardrail text and correct XML
      section order
  - to: prompt-transport-contract
    relation: implements
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle define how
      prompts reach engine CLIs (STDIN vs argv)
  - to: set-e-shape-lint
    relation: validates
    description: >-
      test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action
      pattern that caused APP-240
  - to: tier-ladder-selection
    relation: implements
    description: apply_tier_ladder() selects engine tier from daily budget
generator:
  version: 1
covers:
  - symbol: _is_fatal_shape
    kind: function
    at: 'tests/test_seteshape_lint.py:L42-L43'
  - symbol: _executable_lines
    kind: function
    at: 'tests/test_seteshape_lint.py:L46-L52'
  - symbol: find_violations
    kind: function
    at: 'tests/test_seteshape_lint.py:L55-L84'
  - symbol: SetEShapeLint
    kind: class
    at: 'tests/test_seteshape_lint.py:L87-L99'
  - symbol: test_no_fatal_test_and_shapes
    kind: method
    at: 'tests/test_seteshape_lint.py:L88-L99'
---
<!-- context:generated:start -->
## Summary

The central orchestration loop (scripts/core/auto-loop.sh) that drives engine cycles (claude/jcode/codex), manages the cycle counter, idle-skip, discretionary budget caps, tier ladder, escalation, prompt assembly/transport, and cycle metadata extraction. Many tests extract its function bodies verbatim via awk/sed to drive the shipping code rather than copies, so any change to function boundaries or extraction patterns breaks tests loudly.

## Related

- implements [[cycle-counter-persistence]] — auto-loop.sh's seed block and persist line define the monotonic cycle counter that test_cycle_counter.sh extracts and drives
- implements [[cycle-metadata-extraction]] — extract_cycle_metadata() parses engine output into CYCLE_TYPE/SUBTYPE/RESULT_TEXT, tested by test_cycle_metadata.sh
- implements [[escalation-one-shot-logic]] — apply_cycle_escalation/_consume_escalation/_directive_is_pending implement the APP-238 one-shot operator escalation
- implements [[idle-skip-mechanism]] — _idle_skip_due and the skip branch implement idle detection and consensus-note wiring
- implements [[prompt-assembly-contract]] — FULL_PROMPT assignments must assemble with guardrail text and correct XML section order
- implements [[prompt-transport-contract]] — run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle define how prompts reach engine CLIs (STDIN vs argv)
- validates [[set-e-shape-lint]] — test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action pattern that caused APP-240
- implements [[tier-ladder-selection]] — apply_tier_ladder() selects engine tier from daily budget
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
