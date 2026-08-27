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
- [airtable-queue-watchers](airtable-queue-watchers.md) — Airtable queue watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [analyst-engine-runner](analyst-engine-runner.md) — Analyst engine runner · scripts/analyst/opportunity-analyst-jcode.sh, tests/test_analyst_engine.sh
- [analyst-tooling](analyst-tooling.md) — Analyst Tooling · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/jcode-pilot-smoke.sh, scripts/core/bridge_leak_scan.py
- [atomic-write-and-compare-and-swap-discipline](atomic-write-and-compare-and-swap-discipline.md) — Atomic write and compare-and-swap discipline · scripts/core/directive_writer.py, scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/core/operator_request_notify.py, scripts/ops/cost-audit.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [auto-company-loop-core](auto-company-loop-core.md) — Auto Company loop core · scripts/core/auto-loop.sh, scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — auto_loop · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [auto-loop-orchestration-core](auto-loop-orchestration-core.md) — Auto-loop orchestration core · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [browser-context-extraction](browser-context-extraction.md) — Browser/context extraction · scripts/ops/browse-extract.py, scripts/ops/kik-decision-read.py
- [budget-and-spend-accounting](budget-and-spend-accounting.md) — Budget and spend accounting · scripts/core/auto-loop.sh, scripts/core/engine-usage-cost.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cost_model_hint.sh, tests/test_discretionary_budget.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py
- [cockpit-server](cockpit-server.md) — Cockpit Server · dashboard/server.py
- [compact-ritual-and-directive-integrity](compact-ritual-and-directive-integrity.md) — Compact ritual and directive integrity · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py, scripts/core/directive_writer.py, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh, tests/test_directive_section_refs.sh
- [compact-ritual-hooks](compact-ritual-hooks.md) — Compact Ritual Hooks · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [context-watch](context-watch.md) — Context Watch · scripts/context-watch.py
- [cost-and-budget-accounting](cost-and-budget-accounting.md) — Cost and budget accounting · scripts/core/engine-usage-cost.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py, scripts/ops/operator-usage-report.sh
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py, tests/test_dashboard_server.py
- [decision-content-hash-canonicalization](decision-content-hash-canonicalization.md) — Decision content-hash canonicalization · scripts/core/decision_text_hash.py, scripts/ops/kik-decision-read.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py, scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [engine-final-text-extraction](engine-final-text-extraction.md) — Engine final-text extraction · scripts/core/codex-final-text.py, scripts/core/jcode-final-text.py
- [fail-closed-decision-invariant](fail-closed-decision-invariant.md) — Fail-closed decision invariant · scripts/core/auto-loop.sh, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py, scripts/ops/verify-mcp-keys.py, tests/test_airtable_read.sh, tests/test_ccusage_failclosed.sh
- [fail-open-vs-fail-closed-operational-philosophy](fail-open-vs-fail-closed-operational-philosophy.md) — Fail-open vs fail-closed operational philosophy · scripts/core/directive_writer.py, scripts/core/jcode-mcp-probe.py, scripts/core/telegram-notify.sh, scripts/graft-auto-refresh.py, scripts/ops/bloat-trend.py, scripts/ops/extract-axis-evidence.py, scripts/ops/operator-action-router.py, scripts/ops/registry-archive.py, scripts/ops/reply-watch.py
- [g4-identity-attribution-verification](g4-identity-attribution-verification.md) — G4 identity-attribution verification · scripts/ops/g4-check.py, scripts/ops/site-contact-evidence.py
- [headinspect-inspection-logic](headinspect-inspection-logic.md) — HeadInspect Inspection Logic · projects/headinspect/src/inspect.ts
- [headinspect-renderer](headinspect-renderer.md) — HeadInspect Renderer · projects/headinspect/src/render.ts
- [headinspect-schema](headinspect-schema.md) — HeadInspect Schema · projects/headinspect/migrations/0001_hits.sql
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/src/index.ts
- [infrastructure-and-host-hygiene](infrastructure-and-host-hygiene.md) — Infrastructure and host hygiene · scripts/core/sentry-heartbeat.sh, scripts/ops/docker-prune-safe.sh, scripts/ops/opportunity-analyst-cron.sh
- [linear-workstream-tracking](linear-workstream-tracking.md) — Linear workstream tracking · scripts/ops/linear-track.py
- [mcp-config-generation-and-probe](mcp-config-generation-and-probe.md) — MCP config generation and probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [mcp-configuration-and-probe](mcp-configuration-and-probe.md) — MCP configuration and probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [operator-action-router](operator-action-router.md) — operator_action_router · scripts/ops/operator-action-router.py, tests/test_operator_action_router.py
- [operator-decision-panel-format](operator-decision-panel-format.md) — operator_decision_panel_format · dashboard/server.py, scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [operator-request-notify](operator-request-notify.md) — operator_request_notify · scripts/core/operator_request_notify.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opex-rfq-email-templates](opex-rfq-email-templates.md) — OPEX RFQ email templates · scripts/ops/rfq_template.py
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh
- [ops-archive-and-state](ops-archive-and-state.md) — ops_archive_and_state · scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py, tests/test_registry_archive.sh, tests/test_state_snapshot.sh
- [ops-audit-tools](ops-audit-tools.md) — ops_audit_tools · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [ops-decision-scripts](ops-decision-scripts.md) — Ops decision scripts · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/browse-extract.py, scripts/ops/context7-check.py, scripts/ops/g4-check.py, scripts/ops/idle-skip-note.py, scripts/ops/rfq-send.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py, scripts/ops/state-snapshot.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/verify-mcp-keys.py, scripts/ops/web-research-cost.py
- [ops-watchers](ops-watchers.md) — ops_watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod_mechanism_guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh, tests/test_rfq_send.sh
- [production-mechanism-guard](production-mechanism-guard.md) — Production mechanism guard · scripts/prod-mechanism-guard.py
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [registry-and-evidence-management](registry-and-evidence-management.md) — Registry and evidence management · scripts/ops/extract-axis-evidence.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [rfq-send](rfq-send.md) — rfq_send · scripts/ops/rfq-send.py, tests/test_rfq_send.sh
- [secret-handling-and-env-sourcing](secret-handling-and-env-sourcing.md) — Secret handling and env sourcing · scripts/core/jcode-mcp-config.py, scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh, scripts/ops/linear-track.py, scripts/ops/operator-usage-report.sh
- [secret-handling-convention](secret-handling-convention.md) — Secret handling convention · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [send-gate](send-gate.md) — send_gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-hook](session-brief-hook.md) — Session brief hook · scripts/session-brief.py
- [set-e-shape-lint](set-e-shape-lint.md) — set_e_shape_lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-waitlist](snapog-landing-waitlist.md) — SnapOG Landing & Waitlist · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-og-rendering](snapog-og-rendering.md) — SnapOG OG Rendering · projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/types.ts
- [telegram-notification](telegram-notification.md) — Telegram notification · scripts/core/operator_request_notify.py, scripts/core/telegram-notify.sh, scripts/ops/operator-action-router.py
- [turn-economy-and-bloat-trend-monitoring](turn-economy-and-bloat-trend-monitoring.md) — Turn-economy and bloat trend monitoring · scripts/ops/bloat-trend.py, scripts/ops/context7-check.py
- [wowcar-revenue-model-and-acceptance](wowcar-revenue-model-and-acceptance.md) — Wowcar revenue model and acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary](wowcar-revenue-vocabulary.md) — wowcar_revenue_vocabulary · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

72 per-file wiring cards mirror the source tree under `graft/` (70 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
