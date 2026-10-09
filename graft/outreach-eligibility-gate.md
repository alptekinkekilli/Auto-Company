---
name: Outreach Eligibility Gate
slug: outreach-eligibility-gate
type: system
sources:
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
  - path: scripts/ops/site-contact-evidence.py
    hash: 008b4735e6133445eff667f840f9c7faaeef8013b1363f6555b602a9d6fd048c
sources_digest: 83bbebb16355316c1b2fa6ca43df1b89f78e0c91d74840bba712ca314bcb692a
links:
  - to: airtable-access-wrappers
    relation: uses
    description: Uses the air() wrapper with URL-quoting fix for table names with spaces
  - to: rfq-email-sending-pipeline
    relation: uses
    description: Shares the same eligibility philosophy and Airtable tables for outreach
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
  - symbol: fetch
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L56-L64'
  - symbol: emails
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L67-L68'
  - symbol: looks_unrendered
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L71-L81'
  - symbol: render_dom
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L84-L110'
  - symbol: examine
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L113-L172'
  - symbol: main
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L175-L196'
---
<!-- context:generated:start -->
## Summary

The fail-closed eligibility brake for autonomous outreach: send-gate.py answers 'may this firm be emailed right now?' and exits, never sending itself. Its decide() checks in cheapest-first order daily/total caps (binding on messages not firms), never-send-twice, opt-out, Status='Qualified', unresolved HOLD markers, body-leak scan, and Exclusion limits. Any check that cannot complete is a REFUSE, never an ALLOW. It re-derives G4 by importing g4-check.py and uses site-contact-evidence.py to find a firm's published contact email, where a fetch returning no rendered content is inconclusive, never negative.

## Related

- uses [[airtable-access-wrappers]] — Uses the air() wrapper with URL-quoting fix for table names with spaces
- uses [[rfq-email-sending-pipeline]] — Shares the same eligibility philosophy and Airtable tables for outreach
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
