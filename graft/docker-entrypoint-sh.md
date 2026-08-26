---
name: docker-entrypoint.sh
slug: docker-entrypoint-sh
type: file
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
sources_digest: 4859f8b1dfb24f857df1d999107a7d92d7c4d14a2c247976ae81cbb021029d23
links:
  - to: set-e-shape-lint-tests-test-seteshape-lint-py
    relation: uses
    description: Target of the lint.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Container entrypoint whose runtime.env parser uses a redirect-fed loop form that the set-e lint must not false-positive on.

## Related

- uses [[set-e-shape-lint-tests-test-seteshape-lint-py]] — Target of the lint.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
