---
name: rfq_send
slug: rfq-send
type: system
sources:
  - path: scripts/ops/rfq-send.py
    hash: d687a23a667fca0d00ef63d03ff6a2602b9f75dd634b93fc89ec5e7369180b76
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: 4969f4e38e343d47c053b76e7bc86212ee48cee7525a8b0b4a12948a36c2bbf7
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
