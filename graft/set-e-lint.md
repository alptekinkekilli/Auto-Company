---
name: Set-e lint
slug: set-e-lint
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
  - to: auto-loop-core-engine
    relation: validates
    description: Scans auto-loop.sh for the fatal pattern.
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

The invariant that a `[ test ] && action` list must never be a function's last command or sit immediately before a bare return, because set -e propagates a false test's exit status 1 and kills an unguarded caller (root cause of APP-240). The lint is deliberately narrow to avoid false positives on safe redirect-fed loop forms.

## Related

- validates [[auto-loop-core-engine]] — Scans auto-loop.sh for the fatal pattern.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
