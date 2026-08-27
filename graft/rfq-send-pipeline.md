---
name: RFQ send pipeline
slug: rfq-send-pipeline
type: system
sources:
  - path: scripts/ops/rfq-send.py
    hash: 9f7b4a48afe6563f777bfe314209d32a3bc0343d178e25ecf0a442cac0ced2e5
sources_digest: 9696842896070550e06a9e7dcb65beb83e37f7caf47de5a5fc440ba670db72d4
links:
  - to: airtable-ops-wrappers
    relation: uses
    description: >-
      Reads/writes the dedicated RFQ Airtable table via the air() wrapper and
      marks sends back with _mark_sent.
generator:
  version: 1
covers:
  - symbol: _load_key
    kind: function
    at: 'scripts/ops/rfq-send.py:L90-L111'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/rfq-send.py:L114-L116'
  - symbol: _air
    kind: function
    at: 'scripts/ops/rfq-send.py:L120-L132'
  - symbol: _record
    kind: function
    at: 'scripts/ops/rfq-send.py:L135-L136'
  - symbol: _all_rows
    kind: function
    at: 'scripts/ops/rfq-send.py:L139-L150'
  - symbol: _sponsor_ok
    kind: function
    at: 'scripts/ops/rfq-send.py:L154-L155'
  - symbol: _opted_out
    kind: function
    at: 'scripts/ops/rfq-send.py:L158-L159'
  - symbol: _already_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L162-L163'
  - symbol: _email_of
    kind: function
    at: 'scripts/ops/rfq-send.py:L166-L168'
  - symbol: _caps_now
    kind: function
    at: 'scripts/ops/rfq-send.py:L171-L181'
  - symbol: render
    kind: function
    at: 'scripts/ops/rfq-send.py:L184-L191'
  - symbol: anonymity_scan
    kind: function
    at: 'scripts/ops/rfq-send.py:L194-L199'
  - symbol: decide
    kind: function
    at: 'scripts/ops/rfq-send.py:L202-L224'
  - symbol: _encode_subject
    kind: function
    at: 'scripts/ops/rfq-send.py:L228-L231'
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L234-L249'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L252-L255'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L259-L301'
---
<!-- context:generated:start -->
## Summary

Buyer-side fail-closed CLI that sends anonymous indicative pricing RFQs to vendors via ForwardEmail, gating each Airtable record through a strict chain (opt-out, never-twice, email-only vendors, template/scope validity, anonymity scan, daily/total caps, and the §15 Sponsor İzni checkbox that only a human can set).

## Related

- uses [[airtable-ops-wrappers]] — Reads/writes the dedicated RFQ Airtable table via the air() wrapper and marks sends back with _mark_sent.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
