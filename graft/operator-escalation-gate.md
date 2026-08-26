---
name: Operator Escalation Gate
slug: operator-escalation-gate
type: system
sources:
  - path: scripts/core/operator_request_notify.py
    hash: 422b3f99a0cf654022883399da8d8ae7b28d7a6b7bffc2ddfc68dd4d987217ac
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
sources_digest: 46e0f6bc84f7a28d9573997853e4e109a0d0f48e58514525782fa4de3567426b
links:
  - to: airtable-read-write-wrappers
    relation: uses
    description: >-
      registry-queue-watch.py and reply-watch.py read Airtable queues via the
      REST API.
  - to: telegram-notification-channel
    relation: uses
    description: >-
      All four scripts shell out to scripts/core/telegram-notify.sh for operator
      alerts.
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
  - symbol: read_directive
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L40-L56'
  - symbol: last_line_matching
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L59-L66'
  - symbol: main
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L69-L165'
  - symbol: api_key
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L48-L58'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L61-L77'
  - symbol: main
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L80-L215'
  - symbol: api_key
    kind: function
    at: 'scripts/ops/reply-watch.py:L46-L56'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/reply-watch.py:L59-L74'
  - symbol: notify
    kind: function
    at: 'scripts/ops/reply-watch.py:L77-L91'
  - symbol: first_ts
    kind: function
    at: 'scripts/ops/reply-watch.py:L94-L99'
  - symbol: hours_since
    kind: function
    at: 'scripts/ops/reply-watch.py:L102-L112'
  - symbol: main
    kind: function
    at: 'scripts/ops/reply-watch.py:L115-L142'
  - symbol: classify
    kind: function
    at: 'scripts/ops/reply-watch.py:L145-L223'
---
<!-- context:generated:start -->
## Summary

The deterministic operator-escalation and notification layer: the only component allowed to decide whether an OPREQ block is genuinely new/changed (via SHA-256 material_hash), send Telegram notifications, flip OPEN to RESOLVED through type-specific verification, and regenerate the Awaiting Operator projection. Always exits 0 so it never breaks the calling loop.

## Related

- uses [[airtable-read-write-wrappers]] — registry-queue-watch.py and reply-watch.py read Airtable queues via the REST API.
- uses [[telegram-notification-channel]] — All four scripts shell out to scripts/core/telegram-notify.sh for operator alerts.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
