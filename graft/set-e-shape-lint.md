---
name: set-e-shape-lint
slug: set-e-shape-lint
type: concept
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: b5fb48bb9f058cbbbdb87ad2169a17765cd8169cc3dbaeaa1dcb89241eee57f4
links:
  - to: auto-loop
    relation: validates
    description: auto-loop.sh is a lint target.
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

A fatal bash pattern: a `[ test ] && action` list used as a function's last command or immediately before a bare `return` propagates a false test's exit status 1 and kills an unguarded caller (root cause of APP-240). The lint deliberately skips `done`/`fi`/`esac` terminators and `|| true`/`|| :` tails because set -e exempts the left operand of AND-OR lists.

## Related

- validates [[auto-loop]] — auto-loop.sh is a lint target.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
