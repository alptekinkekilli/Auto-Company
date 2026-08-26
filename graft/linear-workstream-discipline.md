---
name: Linear Workstream Discipline
slug: linear-workstream-discipline
type: file
sources:
  - path: scripts/ops/linear-track.py
    hash: 5a0cc4bf3713dd3351302a4e9ed446432c92217afdbefd6fa9ee87a9ccd4f730
sources_digest: ab4334d9d2bf19461212de4e4796a9e06c905727151e75e3aa148fac2d49e754
links:
  - to: operator-escalation-notification
    relation: uses
    description: >-
      Shares the Keychain/env credential resolution pattern used across ops
      scripts.
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

Enforces a workstream discipline: appends checklist items to one long-lived track issue per workstream instead of opening new issues, with cmd_new only creating a real issue for three hardcoded justifications. Handles Linear's normalization of ticked boxes to uppercase - [X] and refuses ambiguous cmd_done matches.

## Related

- uses [[operator-escalation-notification]] — Shares the Keychain/env credential resolution pattern used across ops scripts.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
