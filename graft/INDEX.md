# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-wrappers](airtable-access-wrappers.md) — Airtable Access Wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [airtable-scoped-access](airtable-scoped-access.md) — Airtable scoped access · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [analyst-engine](analyst-engine.md) — Analyst Engine · scripts/analyst/opportunity-analyst-jcode.sh, tests/test_analyst_engine.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-engine](auto-loop-core-engine.md) — auto-loop core engine · scripts/core/auto-loop.sh
- [auto-loop-harness](auto-loop-harness.md) — Auto-Loop Harness · scripts/core/auto-loop.sh, scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh, tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh
- [auto-loop-orchestration](auto-loop-orchestration.md) — Auto-loop orchestration · scripts/core/codex-final-text.py, scripts/core/jcode-final-text.py, scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/ops/bloat-trend.py, scripts/ops/cost-audit.py, scripts/ops/idle-skip-note.py
- [autonomous-loop-orchestrator](autonomous-loop-orchestrator.md) — Autonomous Loop Orchestrator · scripts/core/auto-loop.sh
- [axis-evidence-extraction](axis-evidence-extraction.md) — Axis evidence extraction · scripts/ops/extract-axis-evidence.py
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge leak scanner · scripts/core/bridge_leak_scan.py
- [browser-extraction](browser-extraction.md) — Browser Extraction · scripts/ops/browse-extract.py, tests/test_browse_extract.sh
- [browser-extraction-harness](browser-extraction-harness.md) — Browser extraction harness · scripts/ops/browse-extract.py
- [budget-calibration-report](budget-calibration-report.md) — Budget calibration report · scripts/ops/budget-calibration-report.py, scripts/ops/operator-usage-report.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [compact-ritual](compact-ritual.md) — Compact Ritual · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py, scripts/session-brief.py, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh, tests/test_compact_yol.py
- [compact-ritual-tooling](compact-ritual-tooling.md) — Compact Ritual Tooling · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [consensus-and-registry-maintenance](consensus-and-registry-maintenance.md) — Consensus and registry maintenance · scripts/ops/consensus-prune.py, scripts/ops/registry-archive.py
- [container-bootstrap](container-bootstrap.md) — Container Bootstrap · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-hash provenance · scripts/core/decision_text_hash.py, scripts/ops/kik-decision-read.py
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [context7-compliance-checker](context7-compliance-checker.md) — Context7 compliance checker · scripts/ops/context7-check.py
- [context7-docs-wrapper](context7-docs-wrapper.md) — Context7 Docs Wrapper · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
- [cost-audit](cost-audit.md) — Cost audit · scripts/ops/cost-audit.py
- [cycle-counter-persistence](cycle-counter-persistence.md) — cycle-counter persistence · scripts/core/auto-loop.sh, tests/test_cycle_counter.sh, tests/test_tool_usage_audit.sh
- [cycle-economics-auditing](cycle-economics-auditing.md) — Cycle Economics Auditing · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py, tests/test_cost_audit_tool_surface.py
- [cycle-escalation-brakes](cycle-escalation-brakes.md) — Cycle Escalation Brakes · scripts/ops/turn-bloat-brake.py, scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py, tests/test_auto_loop_ledger_guard.sh, tests/test_auto_loop_work_window.sh
- [cycle-metadata-extraction](cycle-metadata-extraction.md) — cycle metadata extraction · scripts/core/auto-loop.sh, scripts/core/codex-final-text.py, tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-server](dashboard-server.md) — dashboard server · dashboard/server.py, tests/test_dashboard_server.py
- [directive-rule-sweep](directive-rule-sweep.md) — Directive rule sweep · scripts/ops/directive-rule-sweep.py
- [directive-staleness-watcher](directive-staleness-watcher.md) — Directive staleness watcher · scripts/ops/directive-staleness-watch.py
- [directive-write-gate](directive-write-gate.md) — Directive Write Gate · dashboard/server.py, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [directive-writer](directive-writer.md) — directive writer · scripts/core/directive_writer.py, tests/test_directive_section_refs.sh
- [discretionary-budget](discretionary-budget.md) — discretionary budget · scripts/core/auto-loop.sh, tests/test_discretionary_budget.sh
- [docker-disk-guard](docker-disk-guard.md) — Docker disk guard · scripts/ops/docker-prune-safe.sh
- [engine-usage-cost-adapter](engine-usage-cost-adapter.md) — Engine usage cost adapter · scripts/core/engine-usage-cost.py
- [escalation-one-shot](escalation-one-shot.md) — escalation one-shot · scripts/core/auto-loop.sh, tests/test_escalation.sh
- [fail-closed-eligibility-gates](fail-closed-eligibility-gates.md) — Fail-Closed Eligibility Gates · scripts/ops/rfq-send.py, scripts/ops/send-gate.py
- [final-text-extraction](final-text-extraction.md) — Final-text extraction · scripts/core/codex-final-text.py, scripts/core/jcode-final-text.py
- [g4-attribution-evidence](g4-attribution-evidence.md) — G4 Attribution Evidence · scripts/ops/site-contact-evidence.py
- [g4-check](g4-check.md) — G4 check · scripts/ops/g4-check.py, tests/test_g4_check.sh
- [g4-identity-verification](g4-identity-verification.md) — G4 identity verification · scripts/ops/g4-check.py
- [graft-auto-refresh-hook](graft-auto-refresh-hook.md) — Graft auto-refresh hook · scripts/graft-auto-refresh.py
- [headinspect-service](headinspect-service.md) — HeadInspect Service · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [human-directive-writer](human-directive-writer.md) — Human directive writer · scripts/core/directive_writer.py
- [idle-skip-audit-trail](idle-skip-audit-trail.md) — Idle-skip audit trail · scripts/ops/idle-skip-note.py
- [idle-skip-mechanism](idle-skip-mechanism.md) — idle-skip mechanism · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, tests/test_discretionary_budget.sh, tests/test_idle_skip.sh
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-decision-reader](ki-k-decision-reader.md) — KİK decision reader · scripts/ops/kik-decision-read.py
- [ledger-guard](ledger-guard.md) — ledger guard · scripts/ops/ledger-guard.py, tests/test_ledger_guard.py
- [ledger-integrity-guard](ledger-integrity-guard.md) — Ledger integrity guard · scripts/ops/ledger-guard.py
- [linear-workstream-tracker](linear-workstream-tracker.md) — Linear workstream tracker · scripts/ops/linear-track.py
- [loop-monitoring-and-lifecycle](loop-monitoring-and-lifecycle.md) — Loop monitoring and lifecycle · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh
- [mcp-config-generation-and-probe](mcp-config-generation-and-probe.md) — MCP config generation and probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-config-sync](mcp-config-sync.md) — MCP config sync · scripts/core/auto-loop.sh, scripts/core/jcode-mcp-config.py, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_probe.sh
- [mcp-key-fallback](mcp-key-fallback.md) — MCP key fallback · scripts/core/jcode-mcp-config.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [mcp-probe](mcp-probe.md) — MCP probe · scripts/core/jcode-mcp-probe.py, tests/fixtures/mock_mcp_server.py, tests/test_mcp_probe.sh
- [mcp-runtime-verification](mcp-runtime-verification.md) — MCP & Runtime Verification · scripts/ops/context7-check.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_context7_check.sh
- [mixed-harness-attribution](mixed-harness-attribution.md) — mixed-harness attribution · scripts/core/auto-loop.sh, tests/test_mixed_harness.sh
- [operator-action-router](operator-action-router.md) — Operator action router · scripts/ops/operator-action-router.py, tests/test_operator_action_router.py
- [operator-alerting-watchers](operator-alerting-watchers.md) — Operator Alerting Watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py
- [operator-escalation-gate](operator-escalation-gate.md) — Operator escalation gate · scripts/core/operator_request_notify.py
- [operator-request-notify](operator-request-notify.md) — operator request notify · scripts/core/operator_request_notify.py, tests/test_idle_skip.sh, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — Opportunity analyst cron · scripts/ops/opportunity-analyst-cron.sh
- [platform-status-adapters](platform-status-adapters.md) — Platform status adapters · scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh, tests/test_rfq_send.sh
- [production-mechanism-guard](production-mechanism-guard.md) — Production Mechanism Guard · scripts/prod-mechanism-guard.py, tests/test_auto_loop_consensus_prune.sh
- [prompt-assembly](prompt-assembly.md) — prompt assembly · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh
- [prompt-transport-contract](prompt-transport-contract.md) — prompt transport contract · scripts/core/auto-loop.sh, tests/test_prompt_transport.sh
- [refusal-format](refusal-format.md) — refusal format · dashboard/server.py, scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [registry-archive](registry-archive.md) — registry archive · scripts/ops/registry-archive.py, tests/test_registry_archive.sh
- [registry-merge-tool](registry-merge-tool.md) — Registry Merge Tool · scripts/analyst/merge_registry.py
- [registry-queue-watch](registry-queue-watch.md) — registry queue watch · scripts/ops/registry-queue-watch.py, tests/test_registry_queue_watch.sh
- [reply-watch](reply-watch.md) — reply watch · scripts/ops/reply-watch.py, tests/test_reply_watch.sh
- [rfq-send-pipeline](rfq-send-pipeline.md) — RFQ Send Pipeline · scripts/ops/rfq_template.py, scripts/ops/rfq-send.py
- [rfq-watchers-and-sender](rfq-watchers-and-sender.md) — RFQ watchers and sender · scripts/ops/rfq-reply-watch.py, scripts/ops/rfq-send.py, tests/test_rfq_reply_watch.sh, tests/test_rfq_send.sh
- [send-gate](send-gate.md) — send gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [set-e-shape-lint](set-e-shape-lint.md) — set -e shape lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard](snapog-landing-dashboard.md) — SnapOG Landing/Dashboard · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [state-snapshot](state-snapshot.md) — state snapshot · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [state-snapshot-consensus](state-snapshot-consensus.md) — State Snapshot & Consensus · scripts/ops/consensus-prune.py, scripts/ops/state-snapshot.py, tests/test_auto_loop_consensus_prune.sh, tests/test_consensus_prune.py
- [telegram-notification-channel](telegram-notification-channel.md) — Telegram notification channel · scripts/core/telegram-notify.sh
- [tier-ladder-budgeting](tier-ladder-budgeting.md) — tier ladder budgeting · scripts/core/auto-loop.sh, tests/test_tier_ladder_daily.sh
- [tool-usage-audit](tool-usage-audit.md) — tool usage audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-bloat-brake](turn-bloat-brake.md) — turn bloat brake · scripts/ops/turn-bloat-brake.py, tests/test_turn_bloat_brake.py
- [turn-economy-audit](turn-economy-audit.md) — turn economy audit · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [turn-economy-trend-watcher](turn-economy-trend-watcher.md) — Turn-economy trend watcher · scripts/ops/bloat-trend.py
- [work-window-brake](work-window-brake.md) — work window brake · scripts/ops/work-window.py, tests/test_work_window.py
- [work-window-watchdog](work-window-watchdog.md) — work window watchdog · scripts/ops/work-window-watchdog.py, tests/test_work_window_watchdog.py
- [wowcar-revenue-relabel-acceptance](wowcar-revenue-relabel-acceptance.md) — Wowcar Revenue Relabel Acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary](wowcar-revenue-vocabulary.md) — wowcar revenue vocabulary · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh

## Files

86 per-file wiring cards mirror the source tree under `graft/` (84 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
