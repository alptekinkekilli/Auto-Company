---
name: set -e AND-OR list safety invariant
slug: set-e-and-or-list-safety-invariant
type: concept
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: c59056f5398f99709a6d2d51a4db793d54ba49e1a5b7988581e96c4d3e8ddb3d
links:
  - to: set-e-shape-lint-tests-test-seteshape-lint-py
    relation: implements
    description: The lint encodes this invariant as regex checks.
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

Cross-cutting invariant: `[ test ] && action` as a function's last command or before a bare `return` propagates a false test's exit status 1 and kills an unguarded caller under `set -e` (root cause of APP-240). The lint deliberately exempts `done`/`fi`/`esac` terminators (set -e exempts the left operand of AND-OR lists) and skips lines ending in `|| true`/`|| :` which force a zero status, to avoid false positives on the safe redirect-fed loop form.

## Related

- implements [[set-e-shape-lint-tests-test-seteshape-lint-py]] — The lint encodes this invariant as regex checks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
