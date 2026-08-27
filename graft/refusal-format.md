---
name: refusal_format
slug: refusal-format
type: concept
sources:
  - path: scripts/core/operator_request_notify.py
    hash: 422b3f99a0cf654022883399da8d8ae7b28d7a6b7bffc2ddfc68dd4d987217ac
  - path: tests/test_refusal_format.sh
    hash: 11bf5e9869e2e573b4a897e4df84053e4f58d759d3073a9e058705482cc31ef5
sources_digest: 647824c22a2ce72452b1929aad7509baa62caec7e781d4f7e1533a051e8975a9
links:
  - to: operator-request-notify
    relation: validates
    description: >-
      test_refusal_format runs operator_request_notify.py and asserts REFUSED
      status, single audit entry, and idempotent second run.
generator:
  version: 1
covers:
  - symbol: _looks_secret
    kind: function
    at: 'scripts/core/operator_request_notify.py:L114-L123'
  - symbol: now_iso
    kind: function
    at: 'scripts/core/operator_request_notify.py:L134-L135'
  - symbol: norm_field
    kind: function
    at: 'scripts/core/operator_request_notify.py:L138-L139'
  - symbol: material_hash
    kind: function
    at: 'scripts/core/operator_request_notify.py:L142-L151'
  - symbol: parse_fields
    kind: function
    at: 'scripts/core/operator_request_notify.py:L154-L166'
  - symbol: parse_blocks
    kind: function
    at: 'scripts/core/operator_request_notify.py:L169-L181'
  - symbol: validate_required
    kind: function
    at: 'scripts/core/operator_request_notify.py:L184-L186'
  - symbol: set_field_in_block_body
    kind: function
    at: 'scripts/core/operator_request_notify.py:L189-L198'
  - symbol: set_field_in_text
    kind: function
    at: 'scripts/core/operator_request_notify.py:L201-L208'
  - symbol: scrub_secrets
    kind: function
    at: 'scripts/core/operator_request_notify.py:L211-L216'
  - symbol: compose_message
    kind: function
    at: 'scripts/core/operator_request_notify.py:L241-L271'
  - symbol: send_telegram
    kind: function
    at: 'scripts/core/operator_request_notify.py:L274-L294'
  - symbol: attempt_notify
    kind: function
    at: 'scripts/core/operator_request_notify.py:L297-L306'
  - symbol: load_state
    kind: function
    at: 'scripts/core/operator_request_notify.py:L309-L327'
  - symbol: write_state
    kind: function
    at: 'scripts/core/operator_request_notify.py:L330-L337'
  - symbol: write_text_verified
    kind: function
    at: 'scripts/core/operator_request_notify.py:L340-L342'
  - symbol: audit
    kind: function
    at: 'scripts/core/operator_request_notify.py:L345-L348'
  - symbol: render_projection_body
    kind: function
    at: 'scripts/core/operator_request_notify.py:L351-L366'
  - symbol: splice_projection
    kind: function
    at: 'scripts/core/operator_request_notify.py:L369-L397'
  - symbol: process_notifications
    kind: function
    at: 'scripts/core/operator_request_notify.py:L400-L480'
  - symbol: _resolve_evidence_path
    kind: function
    at: 'scripts/core/operator_request_notify.py:L489-L499'
  - symbol: verify_document_procurement
    kind: function
    at: 'scripts/core/operator_request_notify.py:L502-L578'
  - symbol: verify_credential
    kind: function
    at: 'scripts/core/operator_request_notify.py:L581-L622'
  - symbol: _directive_window_after
    kind: function
    at: 'scripts/core/operator_request_notify.py:L646-L654'
  - symbol: _resolves_block_window
    kind: function
    at: 'scripts/core/operator_request_notify.py:L657-L671'
  - symbol: verify_legal_or_financial_decision
    kind: function
    at: 'scripts/core/operator_request_notify.py:L681-L703'
  - symbol: verify_authorization
    kind: function
    at: 'scripts/core/operator_request_notify.py:L706-L732'
  - symbol: refusal_for
    kind: function
    at: 'scripts/core/operator_request_notify.py:L748-L772'
  - symbol: verify_resolution
    kind: function
    at: 'scripts/core/operator_request_notify.py:L775-L796'
  - symbol: _answer_sources
    kind: function
    at: 'scripts/core/operator_request_notify.py:L799-L817'
  - symbol: process_resolutions
    kind: function
    at: 'scripts/core/operator_request_notify.py:L820-L878'
  - symbol: _main_impl
    kind: function
    at: 'scripts/core/operator_request_notify.py:L881-L973'
  - symbol: main
    kind: function
    at: 'scripts/core/operator_request_notify.py:L976-L988'
---
<!-- context:generated:start -->
## Summary

The operator-decision refusal format: a short single-line REFUSE head followed by verbatim multi-line reasoning, with numbered points preserved as separate lines. A line-anchored regex previously flattened multi-line reasoning into one long line, breaking the parser; the fix split head from body. operator_request_notify.py must mark the request REFUSED, write exactly one audit entry, and be idempotent on re-run.

## Related

- validates [[operator-request-notify]] — test_refusal_format runs operator_request_notify.py and asserts REFUSED status, single audit entry, and idempotent second run.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
