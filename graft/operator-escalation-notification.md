---
name: Operator escalation & notification
slug: operator-escalation-notification
type: system
sources:
  - path: scripts/core/operator_request_notify.py
    hash: 520c01aa1d79e0b5137c42b7ac4fac92b3d0b34e53f2e6cded13dae8a046c92a
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
sources_digest: 9ce589be694283a9a830a01cf9387bec578615dde774dcbf0fb66eafda21613e
links:
  - to: cost-budget-reporting
    relation: produces
    description: >-
      operator-usage-report pushes operator spend data consumed by the
      calibration report.
  - to: mcp-boot-config-generation
    relation: uses
    description: >-
      operator_request_notify and the watchers shell out to telegram-notify.sh
      for delivery.
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
    at: 'scripts/core/operator_request_notify.py:L502-L567'
  - symbol: verify_credential
    kind: function
    at: 'scripts/core/operator_request_notify.py:L570-L611'
  - symbol: _directive_window_after
    kind: function
    at: 'scripts/core/operator_request_notify.py:L635-L643'
  - symbol: verify_legal_or_financial_decision
    kind: function
    at: 'scripts/core/operator_request_notify.py:L649-L671'
  - symbol: verify_authorization
    kind: function
    at: 'scripts/core/operator_request_notify.py:L674-L700'
  - symbol: refusal_for
    kind: function
    at: 'scripts/core/operator_request_notify.py:L716-L740'
  - symbol: verify_resolution
    kind: function
    at: 'scripts/core/operator_request_notify.py:L743-L764'
  - symbol: _answer_sources
    kind: function
    at: 'scripts/core/operator_request_notify.py:L767-L785'
  - symbol: process_resolutions
    kind: function
    at: 'scripts/core/operator_request_notify.py:L788-L846'
  - symbol: _main_impl
    kind: function
    at: 'scripts/core/operator_request_notify.py:L849-L941'
  - symbol: main
    kind: function
    at: 'scripts/core/operator_request_notify.py:L944-L956'
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

Deterministic gates that escalate to a human operator via Telegram and keep the operator-request ledger authoritative. operator_request_notify is the sole writer of notification state and the 'Awaiting Operator' projection, enforcing resolution verification (checksummed evidence, PASS logs, human-directive references). The shell notifiers are deliberately non-intrusive: they never return non-zero and no-op when credentials are unset, so callers can invoke them unconditionally.

## Related

- produces [[cost-budget-reporting]] — operator-usage-report pushes operator spend data consumed by the calibration report.
- uses [[mcp-boot-config-generation]] — operator_request_notify and the watchers shell out to telegram-notify.sh for delivery.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
