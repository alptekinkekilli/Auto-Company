---
name: core bash scripts
slug: core-bash-scripts
type: system
sources:
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 292091da91655d216da4e3a71f0c13ecf5f06a6bfafede45466515bb25166708
links:
  - to: set-e-lint-app-240
    relation: validates
    description: auto-loop.sh and docker-entrypoint.sh are the lint targets.
  - to: tier-ladder-selection
    relation: part_of
    description: apply_tier_ladder() lives in auto-loop.sh.
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

The shell core of the system: auto-loop.sh (the main loop, including the apply_tier_ladder() daily-budget tier selection from APP-263 and the turn-economy policy) and docker-entrypoint.sh (container startup, including a runtime.env parser that uses a redirect-fed loop form). These are the highest-risk scripts because a set -e false-test exit can kill an unguarded caller, which is why they are linted and unit-tested.

## Related

- validates [[set-e-lint-app-240]] — auto-loop.sh and docker-entrypoint.sh are the lint targets.
- part of [[tier-ladder-selection]] — apply_tier_ladder() lives in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
