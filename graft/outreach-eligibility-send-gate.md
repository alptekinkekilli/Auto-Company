---
name: Outreach eligibility & send gate
slug: outreach-eligibility-send-gate
type: system
sources:
  - path: scripts/ops/rfq-send.py
    hash: d687a23a667fca0d00ef63d03ff6a2602b9f75dd634b93fc89ec5e7369180b76
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
sources_digest: 0665e51fbdc1b04a66295e045f70c068654b67dcb392dcdbf1a5d423bb0ecd63
links:
  - to: airtable-read-write-guard-layer
    relation: uses
    description: Both scripts read/write the Airtable tables through the guarded wrappers.
  - to: g4-attribution-evidence-gathering
    relation: uses
    description: >-
      send-gate re-derives G4 by importing g4-check.py and requires an exact
      firm-name match in the Registry Bridge.
generator:
  version: 1
covers:
  - symbol: _load_key
    kind: function
    at: 'scripts/ops/rfq-send.py:L61-L82'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/rfq-send.py:L85-L87'
  - symbol: _air
    kind: function
    at: 'scripts/ops/rfq-send.py:L91-L103'
  - symbol: _record
    kind: function
    at: 'scripts/ops/rfq-send.py:L106-L107'
  - symbol: _all_rows
    kind: function
    at: 'scripts/ops/rfq-send.py:L110-L121'
  - symbol: _sponsor_ok
    kind: function
    at: 'scripts/ops/rfq-send.py:L125-L126'
  - symbol: _opted_out
    kind: function
    at: 'scripts/ops/rfq-send.py:L129-L130'
  - symbol: _already_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L133-L134'
  - symbol: _email_of
    kind: function
    at: 'scripts/ops/rfq-send.py:L137-L139'
  - symbol: _caps_now
    kind: function
    at: 'scripts/ops/rfq-send.py:L142-L152'
  - symbol: render
    kind: function
    at: 'scripts/ops/rfq-send.py:L155-L163'
  - symbol: anonymity_scan
    kind: function
    at: 'scripts/ops/rfq-send.py:L166-L171'
  - symbol: decide
    kind: function
    at: 'scripts/ops/rfq-send.py:L174-L197'
  - symbol: _encode_subject
    kind: function
    at: 'scripts/ops/rfq-send.py:L201-L207'
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L210-L228'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L231-L234'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L238-L280'
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

Fail-closed eligibility brakes for autonomous outreach. send-gate.py answers 'may this firm be emailed now?' with cheapest-first checks (daily/total caps binding on messages not firms, never-send-twice, opt-out, Status=Qualified, HOLD markers, body-leak scan, Exclusion ground limits); rfq-send.py is the actual sender with a §15 sponsor-approval gate that is deliberately last and cannot be set programmatically. Any check that cannot complete is a REFUSE, never an ALLOW.

## Related

- uses [[airtable-read-write-guard-layer]] — Both scripts read/write the Airtable tables through the guarded wrappers.
- uses [[g4-attribution-evidence-gathering]] — send-gate re-derives G4 by importing g4-check.py and requires an exact firm-name match in the Registry Bridge.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
