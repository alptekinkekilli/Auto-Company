---
name: Outreach eligibility & send gate
slug: outreach-eligibility-send-gate
type: system
sources:
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
sources_digest: 5ab131417a8c8279edfc66290905fedf1a1dd1427669fc3449e20dab94f45e26
links:
  - to: airtable-read-write-guards
    relation: uses
    description: >-
      Reads Airtable rows through the air() wrapper with URL-quoting fix for
      table names with spaces.
  - to: contact-evidence-gathering
    relation: uses
    description: >-
      g4_live() depends on site-contact-evidence.py to find a firm's published
      contact email for G4 attribution.
  - to: operator-alerting-watchers
    relation: uses
    description: >-
      The reply watchers and queue watcher complement the send gate by alerting
      on outcomes.
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

The fail-closed eligibility brake for autonomous outreach: send-gate.py answers 'may this firm be emailed right now?' checking cheapest-first daily/total caps (3/day, 20 total, binding on messages not firms), never-send-twice, opt-out, Status='Qualified', HOLD markers, body-leak scan, and the Exclusion ground's length/English limits. Caps derive from the Email log's Sent: entries rather than row counts; any check that cannot complete is a REFUSE, never an ALLOW. g4_live() re-derives G4 by importing g4-check.py with an exact firm-name match in the Registry Bridge.

## Related

- uses [[airtable-read-write-guards]] — Reads Airtable rows through the air() wrapper with URL-quoting fix for table names with spaces.
- uses [[contact-evidence-gathering]] — g4_live() depends on site-contact-evidence.py to find a firm's published contact email for G4 attribution.
- uses [[operator-alerting-watchers]] — The reply watchers and queue watcher complement the send gate by alerting on outcomes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
