---
name: set_e_shape_lint
slug: set-e-shape-lint
type: concept
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: e3103dc607cbc3502d7cf66ff0e032fae35606c99d8bae8d61f841d9295998d0
links:
  - to: auto-loop
    relation: validates
    description: Asserts zero violations in auto-loop.sh and docker-entrypoint.sh.
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

A deliberately narrow lint for a fatal set -e pattern: a '[ test ] && action' list used as a function's last command or immediately before a bare return propagates a false test's exit status 1 and kills an unguarded caller (root cause of APP-240). It deliberately does not flag done/fi/esac terminators (set -e exempts the left operand of AND-OR lists) and skips lines ending in '|| true' or '|| :', to avoid false-positives on the safe redirect-fed loop form in docker-entrypoint.sh's runtime.env parser.

## Related

- validates [[auto-loop]] — Asserts zero violations in auto-loop.sh and docker-entrypoint.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
