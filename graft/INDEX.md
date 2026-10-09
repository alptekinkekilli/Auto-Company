# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [advisory-only-escalation-throttling](advisory-only-escalation-throttling.md) — Advisory-Only Escalation Throttling · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py, scripts/ops/state-snapshot.py
- [airtable-access-layer](airtable-access-layer.md) — Airtable access layer · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [airtable-access-wrappers](airtable-access-wrappers.md) — Airtable Access Wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [atomic-state-file-writes](atomic-state-file-writes.md) — Atomic State File Writes · scripts/ops/consensus-prune.py, scripts/ops/state-snapshot.py, scripts/ops/turn-bloat-brake.py, scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-engine](auto-loop-core-engine.md) — auto-loop core engine · tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [auto-loop-harness-brakes-and-guards](auto-loop-harness-brakes-and-guards.md) — Auto-Loop Harness Brakes and Guards · scripts/ops/ledger-guard.py, scripts/ops/turn-bloat-brake.py, scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py, tests/test_auto_loop_consensus_prune.sh, tests/test_auto_loop_ledger_guard.sh, tests/test_auto_loop_work_window.sh
- [autonomous-loop-orchestrator](autonomous-loop-orchestrator.md) — Autonomous Loop Orchestrator · scripts/core/auto-loop.sh
- [budget-gates-and-spend-accounting](budget-gates-and-spend-accounting.md) — Budget Gates and Spend Accounting · scripts/core/auto-loop.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh
- [business-hours-window-gate](business-hours-window-gate.md) — Business-Hours Window Gate · scripts/core/auto-loop.sh, tests/test_active_window.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [compact-ritual-and-session-brief](compact-ritual-and-session-brief.md) — Compact Ritual and Session Brief · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py, scripts/session-brief.py, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh, tests/test_compact_yol.py
- [compact-ritual-tooling](compact-ritual-tooling.md) — Compact Ritual Tooling · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [consensus-pruning-and-ledger-guard](consensus-pruning-and-ledger-guard.md) — Consensus Pruning and Ledger Guard · scripts/ops/consensus-prune.py, scripts/ops/ledger-guard.py, tests/test_auto_loop_consensus_prune.sh, tests/test_consensus_prune.py
- [container-bootstrap](container-bootstrap.md) — Container Bootstrap · docker-entrypoint.sh
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [context7-docs-wrapper](context7-docs-wrapper.md) — Context7 Docs Wrapper · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
- [cost-budget-accounting](cost-budget-accounting.md) — Cost & budget accounting · scripts/core/engine-usage-cost.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py, scripts/ops/operator-usage-report.sh
- [cycle-cost-and-turn-economics](cycle-cost-and-turn-economics.md) — Cycle Cost and Turn Economics · scripts/ops/cost-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py, tests/test_cost_audit_tool_surface.py, tests/test_cost_model_hint.sh
- [dashboard-server](dashboard-server.md) — dashboard server · tests/test_dashboard_server.py, tests/test_refusal_format.sh
- [directive-lifecycle-operator-escalation](directive-lifecycle-operator-escalation.md) — Directive lifecycle & operator escalation · scripts/core/directive_writer.py, scripts/core/operator_request_notify.py, scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [directive-write-gate](directive-write-gate.md) — Directive Write Gate · dashboard/server.py, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [directive-writer-section-refs](directive-writer-section-refs.md) — directive writer & section refs · tests/test_directive_section_refs.sh
- [evidence-extraction-verification](evidence-extraction-verification.md) — Evidence extraction & verification · scripts/ops/browse-extract.py, scripts/ops/extract-axis-evidence.py
- [fail-closed-verification-philosophy](fail-closed-verification-philosophy.md) — Fail-Closed Verification Philosophy · scripts/core/auto-loop.sh, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py, scripts/ops/work-window.py, tests/test_ccusage_failclosed.sh, tests/test_cost_model_hint.sh
- [final-text-extraction-from-event-streams](final-text-extraction-from-event-streams.md) — Final-text extraction from event streams · scripts/core/codex-final-text.py, scripts/core/jcode-final-text.py
- [g4-check](g4-check.md) — G4 check · tests/test_g4_check.sh
- [g4-identity-verification](g4-identity-verification.md) — G4 identity verification · scripts/ops/g4-check.py
- [headinspect-service](headinspect-service.md) — HeadInspect Service · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [infrastructure-disk-hygiene](infrastructure-disk-hygiene.md) — Infrastructure & disk hygiene · scripts/graft-auto-refresh.py, scripts/ops/docker-prune-safe.sh
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-decision-evidence-pipeline](ki-k-decision-evidence-pipeline.md) — KİK decision evidence pipeline · scripts/core/decision_text_hash.py, scripts/ops/kik-decision-read.py
- [ledger-guard-state-snapshot](ledger-guard-state-snapshot.md) — ledger guard & state snapshot · tests/test_ledger_guard.py, tests/test_state_snapshot.sh
- [linear-workstream-discipline](linear-workstream-discipline.md) — Linear workstream discipline · scripts/ops/linear-track.py
- [loop-lifecycle-monitoring](loop-lifecycle-monitoring.md) — Loop lifecycle & monitoring · scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [mcp-config-generation-boot-probe](mcp-config-generation-boot-probe.md) — MCP config generation & boot probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-config-generator](mcp-config-generator.md) — MCP config generator · tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [mcp-config-sync-invariant](mcp-config-sync-invariant.md) — MCP config sync invariant · tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_probe.sh
- [mcp-key-and-tool-verification](mcp-key-and-tool-verification.md) — MCP Key and Tool Verification · scripts/ops/context7-check.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_context7_check.sh
- [mcp-probe](mcp-probe.md) — MCP probe · tests/test_mcp_probe.sh
- [memory-ledger-integrity-guards](memory-ledger-integrity-guards.md) — Memory & ledger integrity guards · scripts/ops/consensus-prune.py, scripts/ops/ledger-guard.py, scripts/ops/registry-archive.py
- [operator-action-router](operator-action-router.md) — operator action router · tests/test_operator_action_router.py
- [operator-alerting-watchers](operator-alerting-watchers.md) — Operator Alerting Watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py
- [operator-notification-routing](operator-notification-routing.md) — Operator notification & routing · scripts/core/operator_request_notify.py, scripts/core/telegram-notify.sh, scripts/ops/operator-action-router.py
- [operator-request-notification-resolution](operator-request-notification-resolution.md) — operator request notification & resolution · tests/test_operator_action_router.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [outcome-rfq-reply-watchers](outcome-rfq-reply-watchers.md) — outcome & RFQ reply watchers · tests/test_reply_watch.sh, tests/test_rfq_reply_watch.sh
- [outreach-eligibility-gate](outreach-eligibility-gate.md) — Outreach Eligibility Gate · scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod-mechanism guard · tests/test_prod_mechanism_guard.sh, tests/test_rfq_send.sh
- [production-surface-protection](production-surface-protection.md) — Production Surface Protection · scripts/prod-mechanism-guard.py
- [prompt-transport-contract](prompt-transport-contract.md) — prompt transport contract · tests/test_prompt_transport.sh
- [registry-merge-tool](registry-merge-tool.md) — Registry Merge Tool · scripts/analyst/merge_registry.py
- [registry-ops](registry-ops.md) — registry ops · tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [rfq-email-sending-pipeline](rfq-email-sending-pipeline.md) — RFQ Email Sending Pipeline · scripts/ops/rfq_template.py, scripts/ops/rfq-reply-watch.py, scripts/ops/rfq-send.py
- [send-gate-outreach-policy](send-gate-outreach-policy.md) — send gate & outreach policy · tests/test_rfq_send.sh, tests/test_send_gate.sh
- [sentry-heartbeat-crash-loop-detection](sentry-heartbeat-crash-loop-detection.md) — Sentry heartbeat & crash-loop detection · scripts/core/sentry-heartbeat.sh, scripts/ops/opportunity-analyst-cron.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-leak-scanning-evidence-integrity](session-leak-scanning-evidence-integrity.md) — Session-leak scanning & evidence integrity · scripts/core/bridge_leak_scan.py, scripts/core/decision_text_hash.py, scripts/ops/directive-rule-sweep.py
- [set-e-shape-lint](set-e-shape-lint.md) — set -e shape lint · tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard](snapog-landing-dashboard.md) — SnapOG Landing/Dashboard · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [state-snapshot-probe](state-snapshot-probe.md) — State Snapshot Probe · scripts/ops/state-snapshot.py
- [telegram-notification-core](telegram-notification-core.md) — Telegram Notification Core · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py, scripts/ops/turn-bloat-brake.py, scripts/ops/work-window-watchdog.py
- [tool-usage-and-turn-ledgers](tool-usage-and-turn-ledgers.md) — Tool Usage and Turn Ledgers · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [tool-usage-audit](tool-usage-audit.md) — tool usage audit · tests/test_tool_usage_audit.sh
- [turn-economy-bloat-brake](turn-economy-bloat-brake.md) — turn economy & bloat brake · tests/test_turn_audit.sh, tests/test_turn_bloat_brake.py
- [turn-economy-compliance-watchers](turn-economy-compliance-watchers.md) — Turn-economy & compliance watchers · scripts/ops/bloat-trend.py, scripts/ops/context7-check.py, scripts/ops/idle-skip-note.py
- [work-window-watchdog](work-window-watchdog.md) — work window & watchdog · tests/test_work_window_watchdog.py, tests/test_work_window.py
- [wowcar-revenue-relabel-acceptance](wowcar-revenue-relabel-acceptance.md) — Wowcar Revenue Relabel Acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary-acceptance](wowcar-revenue-vocabulary-acceptance.md) — wowcar revenue vocabulary acceptance · tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-systemd-daemon-management](wsl-systemd-daemon-management.md) — WSL Systemd Daemon Management · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

86 per-file wiring cards mirror the source tree under `graft/` (84 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
