---
name: Auto-Loop Core
slug: auto-loop-core
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b7375f132f3e571151b83d045a7716b07dc7f6fa9ea37d0788c49606d992f842
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_cycle_metadata.sh
    hash: 66a21f12ac379be58cda6db2e98c410b11104c0fc2c2d8c6efdffd422dcd3988
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
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
sources_digest: 36a531a7115121afcc3d5bfcf3f0f4dfc5b1be4b9d9de44fc5cfe1be44eb5e6c
links:
  - to: budget-spend-accounting
    relation: uses
    description: >-
      Calls ccusage, codex ledger, and record_total_spend to enforce budget
      gates; fail-closed on degraded reads.
  - to: engine-adapters
    relation: uses
    description: >-
      run_claude_cycle_cli, run_codex_cycle_cli, run_jcode_cycle transport
      prompts and attribute cycle metadata/cost per engine.
  - to: idle-skip
    relation: uses
    description: >-
      _idle_skip_due and idle-skip-note.py consensus note gate off-hours
      behavior.
  - to: operator-escalation
    relation: uses
    description: >-
      apply_cycle_escalation consumes one-shot operator escalations from
      runtime.env and human-directive.md.
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

The central orchestration loop (scripts/core/auto-loop.sh) plus its many extracted functions: budget gates, cycle metadata extraction, prompt assembly/transport, tier ladder, escalation, idle skip, and engine selection. This is the heart of the system; most tests extract its function bodies verbatim via awk to drive the shipping code.

## Related

- uses [[budget-spend-accounting]] — Calls ccusage, codex ledger, and record_total_spend to enforce budget gates; fail-closed on degraded reads.
- uses [[engine-adapters]] — run_claude_cycle_cli, run_codex_cycle_cli, run_jcode_cycle transport prompts and attribute cycle metadata/cost per engine.
- uses [[idle-skip]] — _idle_skip_due and idle-skip-note.py consensus note gate off-hours behavior.
- uses [[operator-escalation]] — apply_cycle_escalation consumes one-shot operator escalations from runtime.env and human-directive.md.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
