---
name: Telegram notification
slug: telegram-notification
type: system
sources:
  - path: scripts/core/operator_request_notify.py
    hash: 422b3f99a0cf654022883399da8d8ae7b28d7a6b7bffc2ddfc68dd4d987217ac
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
  - path: scripts/ops/operator-action-router.py
    hash: 25fd8206f44d0baa7b87a910d0d1846fe5ef1b155289d1a769994aff6817587e
sources_digest: dabee0071b966d5a826abe2a2e15ac52f10f2389a8f08f85bb4afda4ed27ff9e
links:
  - to: auto-company-loop-core
    relation: part_of
    description: The loop and its helpers call telegram-notify.sh for operator alerts.
  - to: directive-writer
    relation: uses
    description: >-
      operator_request_notify.py and directive-staleness-watch.py send
      directive/OPREQ alerts through this channel.
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
  - symbol: _now
    kind: function
    at: 'scripts/ops/operator-action-router.py:L78-L79'
  - symbol: read_hold
    kind: function
    at: 'scripts/ops/operator-action-router.py:L82-L102'
  - symbol: read_opreqs
    kind: function
    at: 'scripts/ops/operator-action-router.py:L105-L118'
  - symbol: read_directive
    kind: function
    at: 'scripts/ops/operator-action-router.py:L121-L134'
  - symbol: collect_items
    kind: function
    at: 'scripts/ops/operator-action-router.py:L137-L174'
  - symbol: render
    kind: function
    at: 'scripts/ops/operator-action-router.py:L177-L183'
  - symbol: set_hash
    kind: function
    at: 'scripts/ops/operator-action-router.py:L186-L189'
  - symbol: should_notify
    kind: function
    at: 'scripts/ops/operator-action-router.py:L192-L207'
  - symbol: load_state
    kind: function
    at: 'scripts/ops/operator-action-router.py:L210-L214'
  - symbol: write_state
    kind: function
    at: 'scripts/ops/operator-action-router.py:L217-L225'
  - symbol: clear_state
    kind: function
    at: 'scripts/ops/operator-action-router.py:L228-L232'
  - symbol: notify
    kind: function
    at: 'scripts/ops/operator-action-router.py:L235-L251'
  - symbol: main
    kind: function
    at: 'scripts/ops/operator-action-router.py:L254-L296'
---
<!-- context:generated:start -->
## Summary

The shared real-time operator notification channel. A defensive bash wrapper (telegram-notify.sh) that is safe to call unconditionally — exits silently if credentials are unset, never returns non-zero, truncates to 3900 chars — plus the deterministic operator-escalation gate (operator_request_notify.py) that is the only component allowed to decide whether an OPREQ is genuinely new/changed and to send notifications.

## Related

- part of [[auto-company-loop-core]] — The loop and its helpers call telegram-notify.sh for operator alerts.
- uses [[directive-writer]] — operator_request_notify.py and directive-staleness-watch.py send directive/OPREQ alerts through this channel.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
