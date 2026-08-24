---
name: set -e Safety
slug: set-e-safety
type: concept
sources:
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
sources_digest: e8ab37db2c203d6fd9efb02ce90da3390e76554204c3c71fa7f70f6eb9adeb7f
links:
  - to: test-by-extraction
    relation: implements
    description: The lint scans extracted function bodies for the fatal shape.
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

A lint and test discipline guarding against the fatal `[ test ] && action` pattern that propagates a false test's exit status 1 and kills an unguarded caller (root cause of APP-240). The lint is deliberately narrow to avoid false positives on safe AND-OR and || true forms.

## Related

- implements [[test-by-extraction]] — The lint scans extracted function bodies for the fatal shape.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
