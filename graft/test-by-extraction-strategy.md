---
name: test-by-extraction strategy
slug: test-by-extraction-strategy
type: concept
sources:
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_cycle_metadata.sh
    hash: 66a21f12ac379be58cda6db2e98c410b11104c0fc2c2d8c6efdffd422dcd3988
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: 1637959a6f5f0c5d5ddfb4ce6e63bf46e560f6b3e2c1afbe9636b49b4aa8d86d
links:
  - to: auto-loop-core-loop
    relation: validates
    description: Most extraction-based tests target auto-loop.sh functions.
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

The dominant test strategy: extract the real function bodies from auto-loop.sh (and other scripts) via awk/grep/sed and drive them in a sandboxed harness with stubbed binaries (ccusage, jcode, timeout, date, security) and pinned time (BUDGET_NOW_OVERRIDE, FAKE_HOUR). This tests the shipping code, not a copy, and catches regressions like the stray-quote prompt outage that bash -n could not. Tests deliberately use set -uo pipefail (not -e) to allow controlled failures.

## Related

- validates [[auto-loop-core-loop]] — Most extraction-based tests target auto-loop.sh functions.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
