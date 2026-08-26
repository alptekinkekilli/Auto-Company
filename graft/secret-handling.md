---
name: Secret Handling
slug: secret-handling
type: concept
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/core/operator_request_notify.py
    hash: 422b3f99a0cf654022883399da8d8ae7b28d7a6b7bffc2ddfc68dd4d987217ac
  - path: scripts/ops/airtable-read.py
    hash: 148f66145510c90e03256b7b37853122bcd892d51cba67f095ce700a0895e3e2
  - path: scripts/ops/airtable-write.py
    hash: 888d408c392193511145e11dfbe73841a6d7e3e743e396ab8c8fee8b9507ab7c
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: 1610587b4520951d7aebfb9e38d6bd4e415ebbb7174b5431e84cc041b2bff189
links: []
generator:
  version: 1
covers:
  - symbol: expand
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L82-L94'
  - symbol: sub
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L86-L91'
  - symbol: convert
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L97-L148'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L151-L258'
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
  - symbol: Refusal
    kind: class
    at: 'scripts/ops/airtable-read.py:L68-L69'
  - symbol: load_env
    kind: function
    at: 'scripts/ops/airtable-read.py:L72-L92'
  - symbol: load_keychain
    kind: function
    at: 'scripts/ops/airtable-read.py:L95-L111'
  - symbol: build_params
    kind: function
    at: 'scripts/ops/airtable-read.py:L114-L173'
  - symbol: encode
    kind: function
    at: 'scripts/ops/airtable-read.py:L176-L183'
  - symbol: to_body
    kind: function
    at: 'scripts/ops/airtable-read.py:L186-L198'
  - symbol: request
    kind: function
    at: 'scripts/ops/airtable-read.py:L201-L217'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/airtable-read.py:L220-L239'
  - symbol: clip
    kind: function
    at: 'scripts/ops/airtable-read.py:L242-L248'
  - symbol: main
    kind: function
    at: 'scripts/ops/airtable-read.py:L251-L343'
  - symbol: load_env
    kind: function
    at: 'scripts/ops/airtable-write.py:L46-L62'
  - symbol: load_keychain
    kind: function
    at: 'scripts/ops/airtable-write.py:L65-L80'
  - symbol: call
    kind: function
    at: 'scripts/ops/airtable-write.py:L83-L92'
  - symbol: guard
    kind: function
    at: 'scripts/ops/airtable-write.py:L98-L133'
  - symbol: show
    kind: function
    at: 'scripts/ops/airtable-write.py:L136-L142'
  - symbol: main
    kind: function
    at: 'scripts/ops/airtable-write.py:L145-L202'
---
<!-- context:generated:start -->
## Summary

A cross-cutting security invariant: secrets are never passed as argv or printed, and are loaded from logs/runtime.env or macOS Keychain. airtable-write.py and airtable-read.py load via load_env/load_keychain; jcode-mcp-config.py keeps header secrets unexpanded in argv to avoid ps leaks; docker-prune-safe.sh avoids dot-sourcing runtime.env because values contain '|'; scrub_secrets in operator_request_notify.py is shape-based to avoid stripping request IDs.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
