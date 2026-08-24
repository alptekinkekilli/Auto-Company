---
name: KİK & Linear workstream tooling
slug: ki-k-linear-workstream-tooling
type: system
sources:
  - path: scripts/ops/kik-decision-read.py
    hash: 4f2060cbaaa784433de9720f1e9a3bfb3ba6c06cab00fae0efa0a426e5c926de
  - path: scripts/ops/linear-track.py
    hash: 5a0cc4bf3713dd3351302a4e9ed446432c92217afdbefd6fa9ee87a9ccd4f730
sources_digest: d3e2f6dbe011cf22e28742acea93fc0a1a4170d3d1a27ea034bf85793b5ef6a5
links:
  - to: outreach-eligibility-g4-verification
    relation: uses
    description: >-
      KİK decisions and Linear tracks carry evidence used in G4/attribution and
      escalation.
generator:
  version: 1
covers:
  - symbol: _hasher
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L45-L51'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L54-L67'
  - symbol: text_of
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L70-L73'
  - symbol: first
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L76-L78'
  - symbol: field
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L81-L89'
  - symbol: read
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L92-L131'
  - symbol: main
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L134-L159'
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

Single-call fetchers and workstream discipline tools. kik-decision-read.py pulls a Turkish procurement decision page in one curl call (urllib fails TLS on macOS), parsing exact header patterns and dropping quoted legislation so a quoted article is never mistaken for a real exclusion. linear-track.py enforces appending checklist items to long-lived track issues instead of opening new issues, refusing ambiguous cmd_done matches and only creating real issues for three hardcoded justifications.

## Related

- uses [[outreach-eligibility-g4-verification]] — KİK decisions and Linear tracks carry evidence used in G4/attribution and escalation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
