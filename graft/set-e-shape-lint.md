---
name: set -e shape lint
slug: set-e-shape-lint
type: concept
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: f9a496f4e0fe5319a1b11b70edca4497d399b48d59de2f5764db20f3451464d6
links:
  - to: auto-loop-core-loop
    relation: validates
    description: Lints auto-loop.sh and docker-entrypoint.sh for the fatal set -e shape.
  - to: test-by-extraction-strategy
    relation: part_of
    description: It is one of the extraction-based test tools.
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

A narrow lint (test_seteshape_lint.py) that flags the fatal `[ test ] && action` pattern used as a function's last command or before a bare return, which propagates a false test's exit 1 and kills an unguarded caller (root cause of APP-240). Deliberately does not flag done/fi/esac terminators (set -e exempts the left operand of AND-OR lists) or lines ending in || true/|| :, to avoid false positives on the safe redirect-fed loop form.

## Related

- validates [[auto-loop-core-loop]] — Lints auto-loop.sh and docker-entrypoint.sh for the fatal set -e shape.
- part of [[test-by-extraction-strategy]] — It is one of the extraction-based test tools.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
