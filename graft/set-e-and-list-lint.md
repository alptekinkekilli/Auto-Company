---
name: set -e AND-list lint
slug: set-e-and-list-lint
type: concept
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: f34828fb9fb35392a978b6e6469ddd81d06464603262049c62217e8a31b968d5
links:
  - to: auto-loop-core
    relation: validates
    description: The lint scans auto-loop.sh for the fatal pattern.
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

A deliberately narrow lint (in tests/test_seteshape_lint.py) that flags the fatal `[ test ] && action` shape when it is a function's last command or immediately before a bare return, because a false test propagates exit status 1 and kills an unguarded caller under set -e (root cause of APP-240). It deliberately does not flag done/fi/esac terminators (set -e exempts the left operand of AND-OR lists) nor lines ending in || true / || :, to avoid false-positives on the safe redirect-fed loop form in docker-entrypoint.sh's runtime.env parser.

## Related

- validates [[auto-loop-core]] — The lint scans auto-loop.sh for the fatal pattern.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
