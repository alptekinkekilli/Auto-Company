---
name: Outreach Eligibility Gate (send-gate)
slug: outreach-eligibility-gate-send-gate
type: file
sources:
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
sources_digest: 5ab131417a8c8279edfc66290905fedf1a1dd1427669fc3449e20dab94f45e26
links:
  - to: airtable-access-wrappers
    relation: uses
    description: >-
      Talks to Airtable via the air() wrapper carrying a URL-quoting fix for
      table names with spaces
  - to: g4-attribution-evidence
    relation: uses
    description: >-
      g4_live() re-derives G4 by importing g4-check.py and requires exact
      firm-name match in Registry Bridge
generator:
  version: 1
covers:
  - symbol: phase_of
    kind: function
    at: 'scripts/ops/send-gate.py:L66-L91'
  - symbol: body_claims
    kind: function
    at: 'scripts/ops/send-gate.py:L94-L101'
  - symbol: load_key
    kind: function
    at: 'scripts/ops/send-gate.py:L104-L122'
  - symbol: air
    kind: function
    at: 'scripts/ops/send-gate.py:L125-L135'
  - symbol: sent_rows
    kind: function
    at: 'scripts/ops/send-gate.py:L138-L148'
  - symbol: logged_sends
    kind: function
    at: 'scripts/ops/send-gate.py:L154-L177'
  - symbol: counts
    kind: function
    at: 'scripts/ops/send-gate.py:L180-L198'
  - symbol: opted_out
    kind: function
    at: 'scripts/ops/send-gate.py:L201-L215'
  - symbol: body_leak_scan
    kind: function
    at: 'scripts/ops/send-gate.py:L236-L244'
  - symbol: g4_live
    kind: function
    at: 'scripts/ops/send-gate.py:L247-L309'
  - symbol: decide
    kind: function
    at: 'scripts/ops/send-gate.py:L312-L544'
  - symbol: main
    kind: function
    at: 'scripts/ops/send-gate.py:L547-L583'
---
<!-- context:generated:start -->
## Summary

A fail-closed eligibility brake answering one question — may this firm be emailed right now? — that exits without ever sending. Its decide() checks in cheapest-first order: daily/total caps (3/day, 20 total, binding on messages not firms), never-send-twice, opt-out, Status='Qualified', unresolved HOLD markers, body-leak scan, and Exclusion limits. Caps are computed by scanning all rows and parsing Sent: entries from the Email log rather than trusting row counts; any check that cannot complete is a REFUSE, never an ALLOW.

## Related

- uses [[airtable-access-wrappers]] — Talks to Airtable via the air() wrapper carrying a URL-quoting fix for table names with spaces
- uses [[g4-attribution-evidence]] — g4_live() re-derives G4 by importing g4-check.py and requires exact firm-name match in Registry Bridge
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
