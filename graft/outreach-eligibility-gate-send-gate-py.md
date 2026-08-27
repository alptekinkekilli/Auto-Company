---
name: Outreach eligibility gate (send-gate.py)
slug: outreach-eligibility-gate-send-gate-py
type: system
sources:
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
sources_digest: 5ab131417a8c8279edfc66290905fedf1a1dd1427669fc3449e20dab94f45e26
links:
  - to: airtable-access-wrapper
    relation: uses
    description: >-
      Talks to Airtable API via air() wrapper with URL-quoting fix for table
      names with spaces.
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

Fail-closed eligibility brake for autonomous outreach. decide() checks caps (3/day, 20 total binding on exposures and log-derived sends), never-send-twice, opt-out, Status=Qualified, HOLD markers, content presence, body-leak scan, and Exclusion ground limits. Any check that cannot complete is REFUSE, never ALLOW. Incident-driven hardening: caps bind on messages not firms, follow-up mode derives attempts from the log, Notes HOLD markers must be stamped resolved.

## Related

- uses [[airtable-access-wrapper]] — Talks to Airtable API via air() wrapper with URL-quoting fix for table names with spaces.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
