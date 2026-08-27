# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-layer](airtable-access-layer.md) — Airtable access layer · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [analyst-engine-escalation](analyst-engine-escalation.md) — Analyst engine & escalation · scripts/analyst/opportunity-analyst-jcode.sh, tests/test_analyst_engine.sh, tests/test_escalation.sh
- [analyst-tooling](analyst-tooling.md) — Analyst Tooling · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/jcode-pilot-smoke.sh, scripts/core/bridge_leak_scan.py
- [audit-telemetry-ledgers](audit-telemetry-ledgers.md) — Audit & telemetry ledgers · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — auto_loop · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [auto-loop-core-engine](auto-loop-core-engine.md) — Auto-loop core engine · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [browse-extraction](browse-extraction.md) — Browse extraction · scripts/ops/browse-extract.py, tests/test_browse_extract.sh
- [budget-spend-accounting](budget-spend-accounting.md) — Budget & spend accounting · scripts/core/engine-usage-cost.py, scripts/ops/web-research-cost.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cost_model_hint.sh, tests/test_discretionary_budget.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py
- [cockpit-server](cockpit-server.md) — Cockpit Server · dashboard/server.py
- [compact-ritual-hooks](compact-ritual-hooks.md) — Compact Ritual Hooks · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [compact-ritual-resume-linting](compact-ritual-resume-linting.md) — Compact ritual & resume linting · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [context-watch](context-watch.md) — Context Watch · scripts/context-watch.py
- [context7-import-audit](context7-import-audit.md) — Context7 import audit · scripts/ops/context7-check.py, tests/test_context7_check.sh
- [cycle-metadata-cost-attribution](cycle-metadata-cost-attribution.md) — Cycle metadata & cost attribution · scripts/core/codex-final-text.py, scripts/core/engine-usage-cost.py, tests/test_cost_model_hint.sh, tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py, tests/test_dashboard_server.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [fail-closed-measurement-invariant](fail-closed-measurement-invariant.md) — Fail-closed measurement invariant · scripts/core/auto-loop.sh, scripts/ops/send-gate.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh
- [g4-attribution-contact-evidence](g4-attribution-contact-evidence.md) — G4 attribution & contact evidence · scripts/ops/g4-check.py, scripts/ops/site-contact-evidence.py, tests/test_g4_check.sh
- [headinspect-inspection-logic](headinspect-inspection-logic.md) — HeadInspect Inspection Logic · projects/headinspect/src/inspect.ts
- [headinspect-renderer](headinspect-renderer.md) — HeadInspect Renderer · projects/headinspect/src/render.ts
- [headinspect-schema](headinspect-schema.md) — HeadInspect Schema · projects/headinspect/migrations/0001_hits.sql
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/src/index.ts
- [idle-skip-off-hours-gating](idle-skip-off-hours-gating.md) — Idle-skip & off-hours gating · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, tests/test_active_window.sh, tests/test_idle_skip.sh
- [mcp-configuration-probe](mcp-configuration-probe.md) — MCP configuration & probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [mcp-key-fallback](mcp-key-fallback.md) — MCP key fallback · tests/test_mcp_key_fallback.sh
- [operator-action-router](operator-action-router.md) — operator_action_router · scripts/ops/operator-action-router.py, tests/test_operator_action_router.py
- [operator-decision-panel-format](operator-decision-panel-format.md) — operator_decision_panel_format · dashboard/server.py, scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [operator-request-notify](operator-request-notify.md) — operator_request_notify · scripts/core/operator_request_notify.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh
- [ops-archive-and-state](ops-archive-and-state.md) — ops_archive_and_state · scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py, tests/test_registry_archive.sh, tests/test_state_snapshot.sh
- [ops-audit-tools](ops-audit-tools.md) — ops_audit_tools · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [ops-watchers](ops-watchers.md) — ops_watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh
- [outreach-eligibility-sending](outreach-eligibility-sending.md) — Outreach eligibility & sending · scripts/ops/rfq-send.py, scripts/ops/send-gate.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod_mechanism_guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh, tests/test_rfq_send.sh
- [production-guard-directive-safety](production-guard-directive-safety.md) — Production guard & directive safety · scripts/core/directive_writer.py, scripts/prod-mechanism-guard.py, tests/test_directive_section_refs.sh
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [rfq-send](rfq-send.md) — rfq_send · scripts/ops/rfq-send.py, tests/test_rfq_send.sh
- [secret-handling-ps-safety](secret-handling-ps-safety.md) — Secret handling & ps-safety · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [send-gate](send-gate.md) — send_gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-context-tooling](session-context-tooling.md) — Session & context tooling · scripts/ops/state-snapshot.py, scripts/session-brief.py, tests/test_idle_skip.sh
- [set-e-shape-lint](set-e-shape-lint.md) — set_e_shape_lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-waitlist](snapog-landing-waitlist.md) — SnapOG Landing & Waitlist · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-og-rendering](snapog-og-rendering.md) — SnapOG OG Rendering · projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot-directive-hashing](state-snapshot-directive-hashing.md) — State snapshot & directive hashing · scripts/ops/state-snapshot.py, tests/test_idle_skip.sh
- [wowcar-revenue-model-acceptance](wowcar-revenue-model-acceptance.md) — Wowcar revenue model & acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary](wowcar-revenue-vocabulary.md) — wowcar_revenue_vocabulary · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

72 per-file wiring cards mirror the source tree under `graft/` (70 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
