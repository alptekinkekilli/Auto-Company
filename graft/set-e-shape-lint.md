---
name: set -e shape lint
slug: set-e-shape-lint
type: concept
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: c3ec89f2e2a2a6d25650258e550e1de45591254f2976e1cc728b205195123f6c
links:
  - to: auto-loop-sh-core-loop
    relation: validates
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

A fatal pattern: a `[ test ] && action` list used as a function's last command or before a bare return propagates exit status 1 and kills an unguarded caller (APP-240 root cause). The lint is deliberately narrow, exempting AND-OR left operands and `|| true`/`|| :` tails.

## Related

- validates [[auto-loop-sh-core-loop]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
