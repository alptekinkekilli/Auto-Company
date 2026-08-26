---
name: auto-loop-core
slug: auto-loop-core
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: scripts/core/directive_writer.py
    hash: 447057795ab4776c589695bd00450009df0af8fff481fa7a68c89244ca93a9a3
  - path: scripts/core/engine-usage-cost.py
    hash: 845b4b8bb9293058e19f610185ec25544170dd0adba7323520f2402ecc499a59
  - path: scripts/core/operator_request_notify.py
    hash: 422b3f99a0cf654022883399da8d8ae7b28d7a6b7bffc2ddfc68dd4d987217ac
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_directive_section_refs.sh
    hash: 413742241d956ae77feb01e20780757ee86fa63f3699e3926a2ddeea81a53a71
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
  - path: tests/test_operator_action_router.py
    hash: 20f6bd56ba2238d0242627275af5749560272630a1212f9f9f22159d655d99ae
  - path: tests/test_operator_request_notify.py
    hash: 07fef3026944da791037a735c7e5cea15cdb4f53eabaecf7affda422400f016f
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: b0dfd86de42a62d5b2a02c17b0522b014d0b58180179c09ae068fe20bfb1f298
links:
  - to: cycle-ndjson-log-format
    relation: produces
    description: >-
      The jcode harness in auto-loop.sh writes the cycle ndjson event streams
      the audit tools parse.
  - to: mcp-key-and-config-management
    relation: depends_on
    description: >-
      Boot preflight requires the generated MCP config and verified keys;
      failures crash-loop the loop.
  - to: ops-audit-and-telemetry-scripts
    relation: produces
    description: The loop's spend ledgers and cycle logs feed the audit and cost tools.
  - to: outreach-ops-scripts
    relation: uses
    description: auto-loop invokes the ops scripts to gate and audit sends.
  - to: set-e-and-list-lint
    relation: validates
    description: >-
      test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action
      pattern.
  - to: tier-ladder-tests
    relation: validates
    description: >-
      test_tier_ladder_daily.sh extracts and tests apply_tier_ladder in
      isolation.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
  - symbol: undefined_section_refs
    kind: function
    at: 'scripts/core/directive_writer.py:L74-L83'
  - symbol: now
    kind: function
    at: 'scripts/core/directive_writer.py:L86-L87'
  - symbol: sha
    kind: function
    at: 'scripts/core/directive_writer.py:L90-L91'
  - symbol: read_live
    kind: function
    at: 'scripts/core/directive_writer.py:L94-L100'
  - symbol: body_of
    kind: function
    at: 'scripts/core/directive_writer.py:L103-L110'
  - symbol: audit
    kind: function
    at: 'scripts/core/directive_writer.py:L113-L119'
  - symbol: _telegram_env
    kind: function
    at: 'scripts/core/directive_writer.py:L122-L145'
  - symbol: notify
    kind: function
    at: 'scripts/core/directive_writer.py:L148-L158'
  - symbol: _why_pending
    kind: function
    at: 'scripts/core/directive_writer.py:L161-L189'
  - symbol: backup
    kind: function
    at: 'scripts/core/directive_writer.py:L192-L206'
  - symbol: normalize_ownership
    kind: function
    at: 'scripts/core/directive_writer.py:L209-L255'
  - symbol: atomic_write
    kind: function
    at: 'scripts/core/directive_writer.py:L258-L270'
  - symbol: verify_written
    kind: function
    at: 'scripts/core/directive_writer.py:L273-L277'
  - symbol: Refused
    kind: class
    at: 'scripts/core/directive_writer.py:L280-L281'
  - symbol: with_lock
    kind: function
    at: 'scripts/core/directive_writer.py:L284-L293'
  - symbol: wrapper
    kind: function
    at: 'scripts/core/directive_writer.py:L285-L292'
  - symbol: cmd_write
    kind: function
    at: 'scripts/core/directive_writer.py:L306-L359'
  - symbol: cmd_status
    kind: function
    at: 'scripts/core/directive_writer.py:L363-L397'
  - symbol: cmd_restore
    kind: function
    at: 'scripts/core/directive_writer.py:L401-L437'
  - symbol: cmd_show
    kind: function
    at: 'scripts/core/directive_writer.py:L440-L445'
  - symbol: main
    kind: function
    at: 'scripts/core/directive_writer.py:L448-L495'
  - symbol: _refuse_forbidden
    kind: function
    at: 'scripts/core/directive_writer.py:L476-L482'
  - symbol: fn
    kind: function
    at: 'scripts/core/directive_writer.py:L477-L481'
  - symbol: _n
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L66-L69'
  - symbol: cost_for
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L72-L110'
  - symbol: main
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L113-L191'
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
  - symbol: check
    kind: function
    at: 'tests/test_operator_action_router.py:L27-L33'
  - symbol: check_true
    kind: function
    at: 'tests/test_operator_action_router.py:L36-L37'
  - symbol: make_app
    kind: function
    at: 'tests/test_operator_action_router.py:L40-L67'
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
    at: 'tests/test_operator_request_notify.py:L73-L777'
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
  - symbol: test_evidence_files_scoped_to_the_resolving_block
    kind: method
    at: 'tests/test_operator_request_notify.py:L736-L766'
  - symbol: test_decision_token_with_digits_and_underscore_resolves
    kind: method
    at: 'tests/test_operator_request_notify.py:L768-L777'
---
<!-- context:generated:start -->
## Summary

The central engine scripts/core/auto-loop.sh and its companion extractors (directive_writer.py, engine-usage-cost.py, operator_request_notify.py, idle-skip-note.py, codex-final-text.py) that drive autonomous cycles: budget gates, cycle counter, escalation, idle skip, prompt assembly/transport, and metadata extraction. Heavily regression-tested by extracting real function bodies via awk so tests drive shipping code, not copies.

## Related

- produces [[cycle-ndjson-log-format]] — The jcode harness in auto-loop.sh writes the cycle ndjson event streams the audit tools parse.
- depends on [[mcp-key-and-config-management]] — Boot preflight requires the generated MCP config and verified keys; failures crash-loop the loop.
- produces [[ops-audit-and-telemetry-scripts]] — The loop's spend ledgers and cycle logs feed the audit and cost tools.
- uses [[outreach-ops-scripts]] — auto-loop invokes the ops scripts to gate and audit sends.
- validates [[set-e-and-list-lint]] — test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action pattern.
- validates [[tier-ladder-tests]] — test_tier_ladder_daily.sh extracts and tests apply_tier_ladder in isolation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
