---
name: rfq_send
slug: rfq-send
type: system
sources:
  - path: scripts/ops/rfq-send.py
    hash: 9f7b4a48afe6563f777bfe314209d32a3bc0343d178e25ecf0a442cac0ced2e5
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: 15e83e3369313edcf69d8eaf92f54d529777d2d8bce6324e06c70c1da0ac3e89
links:
  - to: prod-mechanism-guard
    relation: validates
    description: Must be registered in the guard and pass --check-sync.
  - to: send-gate
    relation: uses
    description: Shares the same fail-closed refusal and anonymity-denylist conventions.
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

scripts/ops/rfq-send.py is a buyer-side RFQ sender with security invariants: a §15 sponsor-approval field and _sponsor_ok function, no G4 gate usage, an ANON_DENY anonymity denylist, and correct Airtable table IDs (RFQ table, not the frozen tender table). It fails closed (ALLOW: 0) on live --report and refuses on §15, form-only detection, and company-name leaks.

## Related

- validates [[prod-mechanism-guard]] — Must be registered in the guard and pass --check-sync.
- uses [[send-gate]] — Shares the same fail-closed refusal and anonymity-denylist conventions.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
