---
name: operator action router
slug: operator-action-router
type: file
sources:
  - path: tests/test_operator_action_router.py
    hash: 20f6bd56ba2238d0242627275af5749560272630a1212f9f9f22159d655d99ae
sources_digest: aee2ab54d4a0bbf378215c19c8cda9f570c978b79187200193ed2def73fcd9ed
links: []
generator:
  version: 1
covers:
  - symbol: check
    kind: function
    at: 'tests/test_operator_action_router.py:L27-L33'
  - symbol: check_true
    kind: function
    at: 'tests/test_operator_action_router.py:L36-L37'
  - symbol: make_app
    kind: function
    at: 'tests/test_operator_action_router.py:L40-L67'
---
<!-- context:generated:start -->
## Summary

operator-action-router.py collects and renders operator-facing items with priority ordering (hold > opreq > directive), staleness floors for directives, dedup within a repeat window, state clearing on empty sets, and fail-soft behavior when memories/ is missing. Renders a digest with Turkish header/footer text.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
