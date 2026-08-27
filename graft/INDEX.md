# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [active-window-gate](active-window-gate.md) — Active window gate · scripts/core/auto-loop.sh, tests/test_active_window.sh
- [airtable-access-layer](airtable-access-layer.md) — Airtable access layer · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [airtable-read-write-guards](airtable-read-write-guards.md) — Airtable read/write guards · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [analyst-engine](analyst-engine.md) — Analyst engine · scripts/analyst/opportunity-analyst-jcode.sh, tests/test_analyst_engine.sh
- [analyst-tooling](analyst-tooling.md) — Analyst Tooling · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/jcode-pilot-smoke.sh, scripts/core/bridge_leak_scan.py
- [auto-company-loop-core](auto-company-loop-core.md) — Auto Company loop core · scripts/core/auto-loop.sh, scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — auto_loop · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [auto-loop-core](auto-loop-core.md) — auto-loop core · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [browse-extract](browse-extract.md) — Browse extract · scripts/ops/browse-extract.py, tests/test_browse_extract.sh
- [browser-extraction-harness](browser-extraction-harness.md) — Browser extraction harness · scripts/ops/browse-extract.py
- [budget-gates](budget-gates.md) — Budget gates · scripts/core/auto-loop.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_discretionary_budget.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py
- [cockpit-server](cockpit-server.md) — Cockpit Server · dashboard/server.py
- [compact-ritual](compact-ritual.md) — Compact ritual · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh
- [compact-ritual-hooks](compact-ritual-hooks.md) — Compact Ritual Hooks · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-hash provenance · scripts/core/decision_text_hash.py, scripts/ops/kik-decision-read.py
- [context-watch](context-watch.md) — Context Watch · scripts/context-watch.py
- [context7-audit](context7-audit.md) — Context7 audit · scripts/ops/context7-check.py, tests/test_context7_check.sh
- [context7-compliance-checker](context7-compliance-checker.md) — Context7 compliance checker · scripts/ops/context7-check.py
- [cost-audit](cost-audit.md) — Cost audit · scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py
- [cycle-analytics-ledger](cycle-analytics-ledger.md) — Cycle analytics ledger · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [cycle-counter-metadata](cycle-counter-metadata.md) — Cycle counter & metadata · scripts/core/auto-loop.sh, scripts/core/codex-final-text.py, tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py, tests/test_dashboard_server.py
- [directive-rule-sweep](directive-rule-sweep.md) — Directive rule sweep · scripts/ops/directive-rule-sweep.py
- [directive-staleness-watcher](directive-staleness-watcher.md) — Directive staleness watcher · scripts/ops/directive-staleness-watch.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py, tests/test_directive_section_refs.sh
- [docker-disk-guard](docker-disk-guard.md) — Docker disk guard · scripts/ops/docker-prune-safe.sh
- [engine-usage-cost](engine-usage-cost.md) — Engine usage cost · scripts/core/engine-usage-cost.py, tests/test_cost_model_hint.sh
- [engine-usage-cost-adapter](engine-usage-cost-adapter.md) — Engine usage cost adapter · scripts/core/engine-usage-cost.py
- [escalation-idle-skip](escalation-idle-skip.md) — Escalation & idle skip · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, tests/test_escalation.sh, tests/test_idle_skip.sh
- [evidence-extraction](evidence-extraction.md) — Evidence extraction · scripts/ops/extract-axis-evidence.py
- [final-text-extraction](final-text-extraction.md) — Final-text extraction · scripts/core/codex-final-text.py, scripts/core/jcode-final-text.py
- [g4-attribution-evidence](g4-attribution-evidence.md) — G4 attribution evidence · scripts/ops/g4-check.py, scripts/ops/site-contact-evidence.py
- [g4-identity-check](g4-identity-check.md) — G4 identity check · scripts/ops/g4-check.py
- [graft-auto-refresh](graft-auto-refresh.md) — Graft auto-refresh · scripts/graft-auto-refresh.py
- [headinspect-inspection-logic](headinspect-inspection-logic.md) — HeadInspect Inspection Logic · projects/headinspect/src/inspect.ts
- [headinspect-renderer](headinspect-renderer.md) — HeadInspect Renderer · projects/headinspect/src/render.ts
- [headinspect-schema](headinspect-schema.md) — HeadInspect Schema · projects/headinspect/migrations/0001_hits.sql
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/src/index.ts
- [human-directive-writer](human-directive-writer.md) — Human directive writer · scripts/core/directive_writer.py
- [idle-skip-note](idle-skip-note.md) — Idle-skip note · scripts/ops/idle-skip-note.py
- [ki-k-decision-reader](ki-k-decision-reader.md) — KİK decision reader · scripts/ops/kik-decision-read.py
- [linear-workstream-tracker](linear-workstream-tracker.md) — Linear workstream tracker · scripts/ops/linear-track.py
- [mcp-config-generation-and-probe](mcp-config-generation-and-probe.md) — MCP config generation and probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-config-probe](mcp-config-probe.md) — MCP config & probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [mcp-key-verification](mcp-key-verification.md) — MCP key verification · scripts/ops/verify-mcp-keys.py
- [mcp-mock-fixture](mcp-mock-fixture.md) — MCP mock fixture · tests/fixtures/mock_mcp_server.py
- [mixed-harness-attribution](mixed-harness-attribution.md) — Mixed harness attribution · scripts/core/auto-loop.sh, tests/test_mixed_harness.sh
- [operator-action-router](operator-action-router.md) — Operator action router · scripts/ops/operator-action-router.py, tests/test_operator_action_router.py
- [operator-decision-panel-format](operator-decision-panel-format.md) — operator_decision_panel_format · dashboard/server.py, scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [operator-escalation-gate](operator-escalation-gate.md) — Operator escalation gate · scripts/core/operator_request_notify.py
- [operator-request-notify](operator-request-notify.md) — operator_request_notify · scripts/core/operator_request_notify.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [operator-usage-reporter](operator-usage-reporter.md) — Operator usage reporter · scripts/ops/operator-usage-report.sh
- [opex-rfq-send-gate](opex-rfq-send-gate.md) — OPEX RFQ send-gate · scripts/ops/rfq-send.py
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — Opportunity Analyst cron · scripts/ops/opportunity-analyst-cron.sh
- [ops-archive-and-state](ops-archive-and-state.md) — ops_archive_and_state · scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py, tests/test_registry_archive.sh, tests/test_state_snapshot.sh
- [ops-audit-tools](ops-audit-tools.md) — ops_audit_tools · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [ops-watchers](ops-watchers.md) — ops_watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh, tests/test_rfq_send.sh
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [registry-archiver](registry-archiver.md) — Registry archiver · scripts/ops/registry-archive.py
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [registry-queue-watch](registry-queue-watch.md) — Registry queue watch · scripts/ops/registry-queue-watch.py
- [reply-watch](reply-watch.md) — Reply watch · scripts/ops/reply-watch.py
- [rfq-outreach-content](rfq-outreach-content.md) — RFQ outreach content · scripts/ops/rfq_template.py
- [rfq-send](rfq-send.md) — rfq_send · scripts/ops/rfq-send.py, tests/test_rfq_send.sh
- [send-gate](send-gate.md) — send_gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-heartbeat](sentry-heartbeat.md) — Sentry heartbeat · scripts/core/sentry-heartbeat.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-hook](session-brief-hook.md) — Session brief hook · scripts/session-brief.py
- [set-e-shape-lint](set-e-shape-lint.md) — set_e_shape_lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [site-contact-evidence](site-contact-evidence.md) — Site contact evidence · scripts/ops/site-contact-evidence.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-waitlist](snapog-landing-waitlist.md) — SnapOG Landing & Waitlist · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-og-rendering](snapog-og-rendering.md) — SnapOG OG Rendering · projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot-probe](state-snapshot-probe.md) — State snapshot probe · scripts/ops/state-snapshot.py
- [telegram-notification](telegram-notification.md) — Telegram notification · scripts/core/telegram-notify.sh
- [tender-send-gate](tender-send-gate.md) — Tender send-gate · scripts/ops/send-gate.py
- [turn-economy-trend-watcher](turn-economy-trend-watcher.md) — Turn-economy trend watcher · scripts/ops/bloat-trend.py
- [wowcar-revenue-relabel-acceptance](wowcar-revenue-relabel-acceptance.md) — Wowcar revenue relabel acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary](wowcar-revenue-vocabulary.md) — wowcar_revenue_vocabulary · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

72 per-file wiring cards mirror the source tree under `graft/` (70 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
