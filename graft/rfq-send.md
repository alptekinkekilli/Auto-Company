---
name: rfq_send
slug: rfq-send
type: system
sources:
  - path: scripts/ops/rfq-send.py
    hash: b5a258fc43421bca16a129c0b3e6d9f1cdefadb4a76cd61623883d74b5667701
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: 56134e4b4b31d1834a370c3d21f077cf6cc59d503b54c53977e91802548ad3d4
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
    at: 'scripts/ops/rfq-send.py:L155-L161'
  - symbol: anonymity_scan
    kind: function
    at: 'scripts/ops/rfq-send.py:L164-L169'
  - symbol: decide
    kind: function
    at: 'scripts/ops/rfq-send.py:L172-L194'
  - symbol: _encode_subject
    kind: function
    at: 'scripts/ops/rfq-send.py:L198-L201'
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L204-L219'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L222-L225'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L229-L271'
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
