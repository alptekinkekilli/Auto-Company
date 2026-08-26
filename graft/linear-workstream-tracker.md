---
name: Linear workstream tracker
slug: linear-workstream-tracker
type: file
sources:
  - path: scripts/ops/linear-track.py
    hash: 5a0cc4bf3713dd3351302a4e9ed446432c92217afdbefd6fa9ee87a9ccd4f730
sources_digest: ab4334d9d2bf19461212de4e4796a9e06c905727151e75e3aa148fac2d49e754
links:
  - to: operator-escalation-gate
    relation: uses
    description: >-
      Tracks APP-269/276/277/246/221 are the same workstreams the escalation
      gate's OPREQs reference.
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

Enforces a workstream discipline for Linear: appends checklist items to one long-lived 'track' issue per workstream instead of opening a new issue per finding. New real issues require one of three hardcoded justifications. Handles Linear's normalization of ticked boxes to uppercase - [X], refuses ambiguous cmd_done matches, and falls back to the macOS Keychain because GUI-launched processes never get the interactive-shell env var.

## Related

- uses [[operator-escalation-gate]] — Tracks APP-269/276/277/246/221 are the same workstreams the escalation gate's OPREQs reference.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
