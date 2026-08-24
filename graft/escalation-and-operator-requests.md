---
name: Escalation and operator requests
slug: escalation-and-operator-requests
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: scripts/core/operator_request_notify.py
    hash: 520c01aa1d79e0b5137c42b7ac4fac92b3d0b34e53f2e6cded13dae8a046c92a
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_operator_request_notify.py
    hash: 2a4ea48a200b3d54e86f5345da91ab5784cc693b6c15991835a485c677ac05c2
  - path: tests/test_refusal_format.sh
    hash: 11bf5e9869e2e573b4a897e4df84053e4f58d759d3073a9e058705482cc31ef5
sources_digest: d9391424c19705e2e1ed6b2320e624c171f81d40b2a4a44a35166b341d1f4649
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: >-
      apply_cycle_escalation and related functions are extracted from
      auto-loop.sh.
  - to: dashboard-server
    relation: produces
    description: >-
      The refusal format written by the cockpit's operator-decision panel is
      consumed by operator_request_notify.py.
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
  - symbol: make_send_fn
    kind: function
    at: 'tests/test_operator_request_notify.py:L40-L50'
  - symbol: _send
    kind: function
    at: 'tests/test_operator_request_notify.py:L44-L47'
  - symbol: block_text
    kind: function
    at: 'tests/test_operator_request_notify.py:L53-L70'
  - symbol: OperatorRequestNotifyTests
    kind: class
    at: 'tests/test_operator_request_notify.py:L73-L734'
  - symbol: setUp
    kind: method
    at: 'tests/test_operator_request_notify.py:L74-L87'
  - symbol: tearDown
    kind: method
    at: 'tests/test_operator_request_notify.py:L89-L91'
  - symbol: write_requests
    kind: method
    at: 'tests/test_operator_request_notify.py:L93-L96'
  - symbol: noop_sleep
    kind: method
    at: 'tests/test_operator_request_notify.py:L98-L99'
  - symbol: test_new_request_notified_once
    kind: method
    at: 'tests/test_operator_request_notify.py:L102-L118'
  - symbol: test_unchanged_request_not_renotified
    kind: method
    at: 'tests/test_operator_request_notify.py:L121-L126'
  - symbol: test_timestamp_only_change_does_not_renotify
    kind: method
    at: 'tests/test_operator_request_notify.py:L129-L138'
  - symbol: test_material_change_renotifies_once
    kind: method
    at: 'tests/test_operator_request_notify.py:L141-L155'
  - symbol: test_ordinary_hold_type_never_notifies
    kind: method
    at: 'tests/test_operator_request_notify.py:L158-L177'
  - symbol: test_telegram_failure_not_marked_notified_then_recovers
    kind: method
    at: 'tests/test_operator_request_notify.py:L180-L195'
  - symbol: test_document_procurement_resolution_verifies_checksum_then_disappears
    kind: method
    at: 'tests/test_operator_request_notify.py:L202-L244'
  - symbol: test_document_procurement_resolution_blocks_on_checksum_mismatch
    kind: method
    at: 'tests/test_operator_request_notify.py:L248-L279'
  - symbol: test_document_procurement_resolution_blocks_path_outside_evidence_dir
    kind: method
    at: 'tests/test_operator_request_notify.py:L283-L308'
  - symbol: test_credential_resolution_requires_pass_log_without_secrets
    kind: method
    at: 'tests/test_operator_request_notify.py:L312-L353'
  - symbol: test_credential_resolution_blocks_if_log_contains_secret_shaped_token
    kind: method
    at: 'tests/test_operator_request_notify.py:L355-L400'
  - symbol: test_legal_decision_resolution_requires_structured_decision_line
    kind: method
    at: 'tests/test_operator_request_notify.py:L405-L435'
  - symbol: test_adjudication_pending_resolution_requires_structured_decision_line
    kind: method
    at: 'tests/test_operator_request_notify.py:L441-L480'
  - symbol: test_expenditure_resolution_requires_structured_authorization_block
    kind: method
    at: 'tests/test_operator_request_notify.py:L485-L523'
  - symbol: test_dedup_state_persists_across_process_reinstantiation
    kind: method
    at: 'tests/test_operator_request_notify.py:L528-L538'
  - symbol: _must_not_be_called
    kind: function
    at: 'tests/test_operator_request_notify.py:L534-L535'
  - symbol: test_requests_md_write_failure_does_not_lose_notified_state
    kind: method
    at: 'tests/test_operator_request_notify.py:L544-L565'
  - symbol: test_authorization_complete_block_passes
    kind: method
    at: 'tests/test_operator_request_notify.py:L585-L588'
  - symbol: test_authorization_blank_field_does_not_borrow_next_line
    kind: method
    at: 'tests/test_operator_request_notify.py:L590-L598'
  - symbol: test_authorization_missing_field_reported
    kind: method
    at: 'tests/test_operator_request_notify.py:L600-L604'
  - symbol: _refuse_run
    kind: method
    at: 'tests/test_operator_request_notify.py:L613-L621'
  - symbol: test_refuse_closes_the_request_as_refused_not_resolved
    kind: method
    at: 'tests/test_operator_request_notify.py:L623-L631'
  - symbol: test_refuse_works_without_an_authorization_block
    kind: method
    at: 'tests/test_operator_request_notify.py:L633-L640'
  - symbol: test_prose_mentioning_refusal_does_not_close_anything
    kind: method
    at: 'tests/test_operator_request_notify.py:L642-L651'
  - symbol: test_bare_refuse_with_two_requests_fails_closed
    kind: method
    at: 'tests/test_operator_request_notify.py:L653-L661'
  - symbol: test_named_refuse_targets_only_that_request
    kind: method
    at: 'tests/test_operator_request_notify.py:L663-L673'
  - symbol: _evidence
    kind: method
    at: 'tests/test_operator_request_notify.py:L683-L689'
  - symbol: test_evidence_files_in_the_directive_resolves
    kind: method
    at: 'tests/test_operator_request_notify.py:L691-L699'
  - symbol: test_evidence_files_in_the_request_block_still_resolves
    kind: method
    at: 'tests/test_operator_request_notify.py:L701-L713'
  - symbol: test_directive_entry_with_a_wrong_checksum_is_rejected
    kind: method
    at: 'tests/test_operator_request_notify.py:L715-L723'
  - symbol: test_directive_entry_cannot_escape_the_evidence_directory
    kind: method
    at: 'tests/test_operator_request_notify.py:L725-L734'
---
<!-- context:generated:start -->
## Summary

One-shot operator escalation (APP-238) and the operator-request notification/resolution lifecycle. Escalation is consumed exactly once; a refusal leaves it ARMED rather than burning an approval. Operator requests are deduped by sha256 content fingerprint, HOLD/informational types never notify, and resolution requires type-specific structured evidence (checksum-matched files, structured Decision/Authorization lines).

## Related

- part of [[auto-loop-core-engine]] — apply_cycle_escalation and related functions are extracted from auto-loop.sh.
- produces [[dashboard-server]] — The refusal format written by the cockpit's operator-decision panel is consumed by operator_request_notify.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
