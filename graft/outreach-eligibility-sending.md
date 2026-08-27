---
name: Outreach eligibility & sending
slug: outreach-eligibility-sending
type: system
sources:
  - path: scripts/ops/rfq-send.py
    hash: 6eba70f90c4ea6f452b170eb3cb7bcfa43a49c1916158db352eb52c9cc503456
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
sources_digest: 5b6ef2c690679aa0919fba18f60f4826f81d6e6545466a3c2637d53ca5c67fc2
links:
  - to: airtable-access-layer
    relation: uses
  - to: g4-attribution-contact-evidence
    relation: uses
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
    at: 'scripts/ops/rfq-send.py:L201-L204'
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L207-L225'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L228-L231'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L235-L277'
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

Fail-closed eligibility brakes and senders for autonomous outreach: send-gate.py answers 'may this firm be emailed now?' and never sends; rfq-send.py sends anonymous OPEX RFQ emails gated by a human-only §15 checkbox. Caps bind on messages not firms, follow-up attempts derive from the log, and any check that cannot complete is a REFUSE, never an ALLOW.

## Related

- uses [[airtable-access-layer]]
- uses [[g4-attribution-contact-evidence]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
