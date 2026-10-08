# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-read-write-guards](airtable-read-write-guards.md) — Airtable read/write guards · tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [airtable-scoped-read-write-wrappers](airtable-scoped-read-write-wrappers.md) — Airtable scoped read/write wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [analyst-engine-provider-routing](analyst-engine-provider-routing.md) — Analyst engine provider routing · tests/test_analyst_engine.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-engine](auto-loop-core-engine.md) — auto-loop core engine · tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [auto-loop-harness-budget-governance](auto-loop-harness-budget-governance.md) — Auto-loop harness & budget governance · tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh
- [auto-loop-orchestration](auto-loop-orchestration.md) — auto-loop orchestration · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh, scripts/graft-auto-refresh.py, scripts/ops/consensus-prune.py, scripts/ops/idle-skip-note.py, scripts/ops/ledger-guard.py
- [autonomous-loop-orchestrator](autonomous-loop-orchestrator.md) — Autonomous Loop Orchestrator · scripts/core/auto-loop.sh
- [browseros-browse-extract-harness](browseros-browse-extract-harness.md) — BrowserOS browse-extract harness · scripts/ops/browse-extract.py
- [budget-calibration-cost-audit](budget-calibration-cost-audit.md) — Budget calibration & cost audit · scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py, scripts/ops/operator-usage-report.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [compact-ritual-tooling](compact-ritual-tooling.md) — Compact Ritual Tooling · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [consensus-ledger-integrity-guards](consensus-ledger-integrity-guards.md) — Consensus & ledger integrity guards · scripts/ops/consensus-prune.py, scripts/ops/idle-skip-note.py, scripts/ops/ledger-guard.py
- [contact-evidence-gathering](contact-evidence-gathering.md) — Contact evidence gathering · scripts/ops/site-contact-evidence.py
- [container-bootstrap](container-bootstrap.md) — Container Bootstrap · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-hash provenance · scripts/core/decision_text_hash.py, scripts/ops/consensus-prune.py, scripts/ops/kik-decision-read.py, scripts/ops/ledger-guard.py
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [context7-compliance-checker](context7-compliance-checker.md) — Context7 compliance checker · scripts/ops/context7-check.py
- [context7-docs-wrapper](context7-docs-wrapper.md) — Context7 Docs Wrapper · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
- [context7-import-audit](context7-import-audit.md) — Context7 import audit · tests/test_context7_check.sh
- [cost-audit-tool-surface](cost-audit-tool-surface.md) — cost audit tool surface · tests/test_cost_audit_tool_surface.py
- [cost-model-hint](cost-model-hint.md) — cost model hint · tests/test_cost_model_hint.sh
- [cycle-counter-persistence](cycle-counter-persistence.md) — cycle counter persistence · tests/test_cycle_counter.sh
- [cycle-metadata-extraction](cycle-metadata-extraction.md) — cycle metadata extraction · tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-server](dashboard-server.md) — dashboard server · tests/test_dashboard_server.py
- [directive-governance-watchers](directive-governance-watchers.md) — Directive governance watchers · scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [directive-write-gate](directive-write-gate.md) — Directive Write Gate · dashboard/server.py, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [directive-writer-section-refs](directive-writer-section-refs.md) — directive writer section refs · tests/test_directive_section_refs.sh
- [discretionary-budget-cap](discretionary-budget-cap.md) — discretionary budget cap · tests/test_discretionary_budget.sh
- [docker-disk-space-guard-docker-prune-safe](docker-disk-space-guard-docker-prune-safe.md) — Docker disk-space guard (docker-prune-safe) · scripts/ops/docker-prune-safe.sh
- [engine-usage-cost-adapter-engine-usage-cost](engine-usage-cost-adapter-engine-usage-cost.md) — Engine usage cost adapter (engine-usage-cost) · scripts/core/engine-usage-cost.py
- [escalation-one-shot-logic](escalation-one-shot-logic.md) — escalation one-shot logic · tests/test_escalation.sh
- [evidence-extraction-g4-verification](evidence-extraction-g4-verification.md) — Evidence extraction & G4 verification · scripts/ops/extract-axis-evidence.py, scripts/ops/g4-check.py
- [fail-closed-atomic-state-writes](fail-closed-atomic-state-writes.md) — Fail-closed atomic state writes · scripts/core/directive_writer.py, scripts/core/jcode-mcp-config.py, scripts/core/operator_request_notify.py, scripts/ops/airtable-write.py, scripts/ops/idle-skip-note.py
- [final-text-extractors-codex-jcode](final-text-extractors-codex-jcode.md) — Final-text extractors (codex/jcode) · scripts/core/codex-final-text.py, scripts/core/jcode-final-text.py
- [g4-check](g4-check.md) — G4 check · tests/test_g4_check.sh
- [graft-auto-refresh-hook](graft-auto-refresh-hook.md) — Graft auto-refresh hook · scripts/graft-auto-refresh.py
- [headinspect-service](headinspect-service.md) — HeadInspect Service · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [human-directive-writer-directive-writer](human-directive-writer-directive-writer.md) — Human-directive writer (directive_writer) · scripts/core/directive_writer.py
- [idle-skip-mechanism](idle-skip-mechanism.md) — idle-skip mechanism · tests/test_discretionary_budget.sh, tests/test_idle_skip.sh
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-decision-content-hash-decision-text-hash](ki-k-decision-content-hash-decision-text-hash.md) — KİK decision content-hash (decision_text_hash) · scripts/core/decision_text_hash.py
- [ki-k-decision-reader](ki-k-decision-reader.md) — KİK decision reader · scripts/ops/kik-decision-read.py
- [ledger-guard](ledger-guard.md) — ledger guard · tests/test_ledger_guard.py
- [linear-workstream-tracker](linear-workstream-tracker.md) — Linear workstream tracker · scripts/ops/linear-track.py
- [loop-lifecycle-monitoring-core-shell](loop-lifecycle-monitoring-core-shell.md) — Loop lifecycle & monitoring (core shell) · scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/core/telegram-notify.sh
- [macos-launchd-daemon-management](macos-launchd-daemon-management.md) — macOS launchd daemon management · scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [mcp-config-generation-boot-probe](mcp-config-generation-boot-probe.md) — MCP config generation & boot probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-configuration-and-manifest-sync](mcp-configuration-and-manifest-sync.md) — MCP configuration and manifest sync · tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [mcp-key-verification](mcp-key-verification.md) — MCP key verification · scripts/ops/verify-mcp-keys.py
- [mcp-probe-determinism](mcp-probe-determinism.md) — MCP probe determinism · tests/test_mcp_probe.sh
- [mcp-probe-test-fixtures](mcp-probe-test-fixtures.md) — MCP probe & test fixtures · tests/fixtures/mock_mcp_server.py, tests/test_browse_extract.sh
- [mcp-secret-in-env-invariant](mcp-secret-in-env-invariant.md) — MCP secret-in-env invariant · tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [operational-guard-tripwires](operational-guard-tripwires.md) — Operational guard tripwires · scripts/ops/turn-bloat-brake.py, scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py, tests/test_auto_loop_consensus_prune.sh, tests/test_auto_loop_ledger_guard.sh, tests/test_auto_loop_work_window.sh, tests/test_consensus_prune.py
- [operator-action-router](operator-action-router.md) — Operator action router · scripts/ops/operator-action-router.py, tests/test_operator_action_router.py
- [operator-alerting-watchers](operator-alerting-watchers.md) — Operator alerting watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py
- [operator-escalation-gate-operator-request-notify](operator-escalation-gate-operator-request-notify.md) — Operator escalation gate (operator_request_notify) · scripts/core/operator_request_notify.py
- [operator-request-notification](operator-request-notification.md) — operator request notification · tests/test_operator_action_router.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — Opportunity Analyst cron · scripts/ops/opportunity-analyst-cron.sh
- [outreach-eligibility-send-gate](outreach-eligibility-send-gate.md) — Outreach eligibility & send gate · scripts/ops/send-gate.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod mechanism guard · tests/test_prod_mechanism_guard.sh, tests/test_rfq_send.sh
- [production-surface-protection](production-surface-protection.md) — Production surface protection · scripts/prod-mechanism-guard.py, tests/test_auto_loop_consensus_prune.sh
- [prompt-assembly-contract](prompt-assembly-contract.md) — prompt assembly contract · tests/test_prompt_assembly.sh
- [prompt-transport-contract](prompt-transport-contract.md) — prompt transport contract · tests/test_prompt_transport.sh
- [refusal-format-contract](refusal-format-contract.md) — refusal format contract · tests/test_refusal_format.sh
- [registry-history-archival](registry-history-archival.md) — Registry history archival · scripts/ops/registry-archive.py
- [registry-merge-tool](registry-merge-tool.md) — Registry Merge Tool · scripts/analyst/merge_registry.py
- [registry-operations](registry-operations.md) — registry operations · tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [reply-watch](reply-watch.md) — reply watch · tests/test_reply_watch.sh
- [rfq-operations](rfq-operations.md) — RFQ operations · tests/test_rfq_reply_watch.sh, tests/test_rfq_send.sh
- [rfq-procurement-flow](rfq-procurement-flow.md) — RFQ procurement flow · scripts/ops/rfq_template.py, scripts/ops/rfq-reply-watch.py, scripts/ops/rfq-send.py
- [send-gate](send-gate.md) — send gate · tests/test_rfq_send.sh, tests/test_send_gate.sh
- [sentry-heartbeat-container-status](sentry-heartbeat-container-status.md) — Sentry heartbeat & container status · scripts/core/sentry-heartbeat.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-compact-ritual](session-brief-compact-ritual.md) — Session brief & compact ritual · scripts/session-brief.py, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh, tests/test_compact_yol.py
- [session-leak-scanner-bridge-leak-scan](session-leak-scanner-bridge-leak-scan.md) — Session-leak scanner (bridge_leak_scan) · scripts/core/bridge_leak_scan.py
- [set-e-shape-lint](set-e-shape-lint.md) — set -e shape lint · tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard](snapog-landing-dashboard.md) — SnapOG Landing/Dashboard · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [state-snapshot-and-delta](state-snapshot-and-delta.md) — state snapshot and DELTA · tests/test_state_snapshot.sh
- [state-snapshot-delta-probing](state-snapshot-delta-probing.md) — State snapshot & delta probing · scripts/ops/state-snapshot.py
- [tier-ladder-selection](tier-ladder-selection.md) — tier ladder selection · tests/test_tier_ladder_daily.sh
- [tool-usage-audit](tool-usage-audit.md) — tool usage audit · tests/test_tool_usage_audit.sh
- [trust-gating-canary-pattern](trust-gating-canary-pattern.md) — Trust-gating canary pattern · scripts/core/bridge_leak_scan.py, scripts/ops/directive-rule-sweep.py
- [turn-economics-auditing](turn-economics-auditing.md) — Turn economics auditing · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [turn-economy-policy](turn-economy-policy.md) — turn economy policy · tests/test_turn_audit.sh, tests/test_turn_bloat_brake.py
- [turn-economy-trend-watcher-bloat-trend](turn-economy-trend-watcher-bloat-trend.md) — Turn-economy trend watcher (bloat-trend) · scripts/ops/bloat-trend.py
- [work-window](work-window.md) — work window · tests/test_work_window.py
- [work-window-bloat-brakes](work-window-bloat-brakes.md) — Work-window & bloat brakes · scripts/ops/turn-bloat-brake.py, scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py, tests/test_auto_loop_work_window.sh
- [work-window-watchdog](work-window-watchdog.md) — work window watchdog · tests/test_work_window_watchdog.py
- [wowcar-revenue-relabel-acceptance](wowcar-revenue-relabel-acceptance.md) — Wowcar revenue relabel acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary](wowcar-revenue-vocabulary.md) — WowCar revenue vocabulary · tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

86 per-file wiring cards mirror the source tree under `graft/` (84 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
