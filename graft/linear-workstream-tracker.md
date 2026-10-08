---
name: Linear workstream tracker
slug: linear-workstream-tracker
type: file
sources:
  - path: scripts/ops/linear-track.py
    hash: 5a0cc4bf3713dd3351302a4e9ed446432c92217afdbefd6fa9ee87a9ccd4f730
sources_digest: ab4334d9d2bf19461212de4e4796a9e06c905727151e75e3aa148fac2d49e754
links:
  - to: operator-action-router
    relation: uses
    description: >-
      operator-action-router.py deliberately excludes Linear-backed queues
      because they need network calls.
generator:
  version: 1
covers:
  - symbol: key
    kind: function
    at: 'scripts/ops/linear-track.py:L65-L79'
  - symbol: gql
    kind: function
    at: 'scripts/ops/linear-track.py:L82-L88'
  - symbol: get_issue
    kind: function
    at: 'scripts/ops/linear-track.py:L91-L97'
  - symbol: set_description
    kind: function
    at: 'scripts/ops/linear-track.py:L100-L102'
  - symbol: cmd_list
    kind: function
    at: 'scripts/ops/linear-track.py:L105-L120'
  - symbol: cmd_add
    kind: function
    at: 'scripts/ops/linear-track.py:L123-L131'
  - symbol: cmd_done
    kind: function
    at: 'scripts/ops/linear-track.py:L134-L145'
  - symbol: cmd_comment
    kind: function
    at: 'scripts/ops/linear-track.py:L148-L152'
  - symbol: cmd_new
    kind: function
    at: 'scripts/ops/linear-track.py:L155-L170'
  - symbol: main
    kind: function
    at: 'scripts/ops/linear-track.py:L173-L196'
---
<!-- context:generated:start -->
## Summary

Enforces a workstream discipline for Linear: appends checklist items to one long-lived 'track' issue per workstream instead of opening a new issue for every finding. cmd_new creates a real issue only if --why matches one of three hardcoded justifications (independent-owner, own-lifecycle, durable-capability). Tracks are hardcoded (APP-269, APP-276, APP-277, APP-246, APP-221). Notable gotchas: Linear normalizes ticked boxes to uppercase - [X] so the list command counts both cases; the Keychain fallback exists because GUI-launched processes never get the interactive-shell env var; cmd_done refuses to tick when zero or multiple items match the needle.

## Related

- uses [[operator-action-router]] — operator-action-router.py deliberately excludes Linear-backed queues because they need network calls.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
