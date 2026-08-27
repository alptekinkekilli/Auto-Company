---
name: OPEX RFQ send-gate
slug: opex-rfq-send-gate
type: system
sources:
  - path: scripts/ops/rfq-send.py
    hash: b5a258fc43421bca16a129c0b3e6d9f1cdefadb4a76cd61623883d74b5667701
sources_digest: cc3d868909cb7d6de20d2f3940cde27a495267925d8ae1feae30f27336ba930c
links: []
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

...
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
