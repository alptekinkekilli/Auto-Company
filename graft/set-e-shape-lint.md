---
name: set -e shape lint
slug: set-e-shape-lint
type: concept
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: 9824d739a8c16a9c17da633b63408b2b7b9e7e2774b57a88b9e2854207b5a193
links:
  - to: auto-loop-sh-core-loop
    relation: validates
    description: >-
      test_seteshape_lint.py asserts zero violations in auto-loop.sh and
      docker-entrypoint.sh.
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

A fatal bash pattern: a `[ test ] && action` list used as a function's last command or immediately before a bare `return` propagates a false test's exit status 1 and kills an unguarded caller (root cause of APP-240). The lint deliberately ignores `done`/`fi`/`esac` terminators and lines ending in `|| true`/`|| :`, which force a zero status, to avoid false positives on the safe redirect-fed loop form.

## Related

- validates [[auto-loop-sh-core-loop]] — test_seteshape_lint.py asserts zero violations in auto-loop.sh and docker-entrypoint.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
