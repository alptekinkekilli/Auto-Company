---
name: RFQ procurement flow
slug: rfq-procurement-flow
type: system
sources:
  - path: scripts/ops/rfq_template.py
    hash: 92801930c70894455bd37f93981ec701390c49b34760c88280fb0ff975bbe5e8
  - path: scripts/ops/rfq-reply-watch.py
    hash: a6ab97903f7cb5a67e749e16ded1a76ba0e022f2faf2e19ce7b0ad094ab441a7
  - path: scripts/ops/rfq-send.py
    hash: 09815061d704b6bd2034469e3bfe3dfac7417f25761ea9ae845be4c5367fd225
sources_digest: 07ca8589e6cadd0d9c4f2ebb8320ea4d59f8be3a891bd9bab62ae638d7dcb348
links:
  - to: airtable-read-write-guards
    relation: uses
    description: Reads/writes the Wowcar OPEX RFQ Airtable table through the wrappers.
  - to: operator-alerting-watchers
    relation: uses
    description: >-
      rfq-reply-watch.py shares the notify/state-file pattern with the other
      watchers.
generator:
  version: 1
covers:
  - symbol: api_key
    kind: function
    at: 'scripts/ops/rfq-reply-watch.py:L36-L46'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/rfq-reply-watch.py:L49-L64'
  - symbol: notify
    kind: function
    at: 'scripts/ops/rfq-reply-watch.py:L67-L80'
  - symbol: first_ts
    kind: function
    at: 'scripts/ops/rfq-reply-watch.py:L83-L88'
  - symbol: hours_since
    kind: function
    at: 'scripts/ops/rfq-reply-watch.py:L91-L106'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-reply-watch.py:L109-L134'
  - symbol: classify
    kind: function
    at: 'scripts/ops/rfq-reply-watch.py:L137-L195'
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
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L201-L226'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L229-L232'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L236-L278'
  - symbol: _read_sig
    kind: function
    at: 'scripts/ops/rfq_template.py:L53-L57'
  - symbol: _logo_b64
    kind: function
    at: 'scripts/ops/rfq_template.py:L60-L62'
  - symbol: _html_signature
    kind: function
    at: 'scripts/ops/rfq_template.py:L68-L76'
  - symbol: attachments
    kind: function
    at: 'scripts/ops/rfq_template.py:L82-L87'
  - symbol: subject
    kind: function
    at: 'scripts/ops/rfq_template.py:L98-L99'
  - symbol: body
    kind: function
    at: 'scripts/ops/rfq_template.py:L102-L119'
  - symbol: body_html
    kind: function
    at: 'scripts/ops/rfq_template.py:L122-L142'
---
<!-- context:generated:start -->
## Summary

The anonymous OPEX RFQ email flow for a hidden client: rfq-send.py is a fail-closed CLI that decides eligibility (opt-out, already-sent, caps, anonymity denylist scan for 'wowcar', and the §15 'Sponsor İzni' checkbox which must be manually TRUE and is deliberately last and unsettable programmatically), renders content from rfq_template.py, and delivers via ForwardEmail. rfq-reply-watch.py is the advisory half that detects new replies or silence (never writes back), and rfq_template.py separates presentation (anonymized scope, logo as CID attachment because Gmail doesn't render base64 data-URIs) from send logic. Form-only vendors are refused because the machine never fills web forms.

## Related

- uses [[airtable-read-write-guards]] — Reads/writes the Wowcar OPEX RFQ Airtable table through the wrappers.
- uses [[operator-alerting-watchers]] — rfq-reply-watch.py shares the notify/state-file pattern with the other watchers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
