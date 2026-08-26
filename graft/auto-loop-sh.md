---
name: auto-loop.sh
slug: auto-loop-sh
type: file
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
sources_digest: b464e67c211c1ff1554e0643aab744e36fe30b6a947596c4b5e9785a9170c824
links:
  - to: set-e-shape-lint-tests-test-seteshape-lint-py
    relation: uses
    description: Target of the lint.
  - to: tier-ladder-daily-tests
    relation: validates
    description: apply_tier_ladder() is extracted and exercised by the harness.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Core orchestration script containing apply_tier_ladder() (daily-budget tier selection, APP-263) and other functions; subject of the set-e shape lint and the tier-ladder test harness.

## Related

- uses [[set-e-shape-lint-tests-test-seteshape-lint-py]] — Target of the lint.
- validates [[tier-ladder-daily-tests]] — apply_tier_ladder() is extracted and exercised by the harness.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
