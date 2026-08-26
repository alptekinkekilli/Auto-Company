---
name: set-e shape lint (tests/test_seteshape_lint.py)
slug: set-e-shape-lint-tests-test-seteshape-lint-py
type: file
sources:
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: bb485dc41fe2695620287c9f61a662378b47a6f7a52a7d87a6d4b941bd639c6c
links:
  - to: auto-loop-sh
    relation: validates
    description: >-
      Lints the apply_tier_ladder and other functions for the fatal set -e
      shape.
  - to: docker-entrypoint-sh
    relation: validates
    description: Lints the runtime.env parser loop form for the fatal set -e shape.
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

Unit test that lints scripts/core/auto-loop.sh and docker-entrypoint.sh for the fatal `[ test ] && action` shape used as a function's last command or before a bare `return`, which propagates a false test's exit 1 and kills an unguarded caller (root cause of APP-240). Uses regexes FUNC_START/TEST_AND/SAFE_TAIL and helpers _is_fatal_shape/_executable_lines; deliberately narrow to avoid false positives on `done`/`fi`/`esac` terminators and `|| true`/`|| :` guards.

## Related

- validates [[auto-loop-sh]] — Lints the apply_tier_ladder and other functions for the fatal set -e shape.
- validates [[docker-entrypoint-sh]] — Lints the runtime.env parser loop form for the fatal set -e shape.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
