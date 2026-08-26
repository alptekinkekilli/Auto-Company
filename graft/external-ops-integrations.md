---
name: External Ops Integrations
slug: external-ops-integrations
type: system
sources:
  - path: scripts/ops/kik-decision-read.py
    hash: 4f2060cbaaa784433de9720f1e9a3bfb3ba6c06cab00fae0efa0a426e5c926de
  - path: scripts/ops/linear-track.py
    hash: 5a0cc4bf3713dd3351302a4e9ed446432c92217afdbefd6fa9ee87a9ccd4f730
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
sources_digest: ca00d31479234af1b1a16525f02f1f2ffbcf4db0026ba19529a90d4d0eaccda7
links:
  - to: cost-budget-ledger-adapters
    relation: uses
    description: >-
      operator-usage-report.sh's blockStart anchors the 5-hour gates and spend
      feeds the 14-day calibration report.
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

One-off operational integrations. linear-track.py enforces a workstream discipline (append checklist items to long-lived track issues, refusing ambiguous matches, only creating real issues for three hardcoded justifications). kik-decision-read.py fetches Turkish procurement decisions in one curl call with a browser user-agent (urllib fails TLS on macOS). operator-usage-report.sh pushes operator Claude usage into the container, with file mtime as the freshness signal.

## Related

- uses [[cost-budget-ledger-adapters]] — operator-usage-report.sh's blockStart anchors the 5-hour gates and spend feeds the 14-day calibration report.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
