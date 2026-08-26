# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-wrappers](airtable-access-wrappers.md) — Airtable access wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [airtable-queue-watchers](airtable-queue-watchers.md) — Airtable Queue Watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [airtable-read-write-wrappers](airtable-read-write-wrappers.md) — Airtable Read/Write Wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [analyst-engine-g4-check](analyst-engine-g4-check.md) — Analyst engine & g4 check · scripts/analyst/opportunity-analyst-jcode.sh, scripts/ops/g4-check.py, tests/test_analyst_engine.sh, tests/test_g4_check.sh
- [atomic-state-writes](atomic-state-writes.md) — Atomic State Writes · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/core/operator_request_notify.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — auto-loop · scripts/core/auto-loop.sh, tests/test_tier_ladder_daily.sh
- [auto-loop-core-engine](auto-loop-core-engine.md) — Auto-loop core engine · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [budget-spend-accounting](budget-spend-accounting.md) — Budget & spend accounting · scripts/core/auto-loop.sh, scripts/core/engine-usage-cost.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cost_model_hint.sh, tests/test_discretionary_budget.sh
- [business-hours-window-gate](business-hours-window-gate.md) — Business-hours window gate · scripts/core/auto-loop.sh, tests/test_active_window.sh
- [cli-final-text-extractors](cli-final-text-extractors.md) — CLI Final-Text Extractors · scripts/core/codex-final-text.py
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py
- [cockpit-server](cockpit-server.md) — Cockpit Server · dashboard/server.py
- [compact-preflight](compact-preflight.md) — Compact Preflight · scripts/compact-preflight.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-Hash Provenance · scripts/core/decision_text_hash.py
- [context-watch](context-watch.md) — Context Watch · scripts/context-watch.py
- [context7-browse-extraction](context7-browse-extraction.md) — Context7 & browse extraction · scripts/ops/browse-extract.py, scripts/ops/context7-check.py, tests/test_browse_extract.sh, tests/test_context7_check.sh
- [cost-budget-ledger-adapters](cost-budget-ledger-adapters.md) — Cost & Budget Ledger Adapters · scripts/core/engine-usage-cost.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py
- [cycle-metadata-mixed-harness-attribution](cycle-metadata-mixed-harness-attribution.md) — Cycle metadata & mixed-harness attribution · scripts/core/auto-loop.sh, scripts/core/codex-final-text.py, tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-cockpit](dashboard-cockpit.md) — Dashboard & cockpit · dashboard/server.py, tests/test_dashboard_server.py, tests/test_refusal_format.sh
- [directive-rule-compliance-watchers](directive-rule-compliance-watchers.md) — Directive & Rule Compliance Watchers · scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [fail-closed-verification-invariant](fail-closed-verification-invariant.md) — Fail-Closed Verification Invariant · scripts/ops/directive-rule-sweep.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [headinspect-service](headinspect-service.md) — HeadInspect Service · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idle-skip-escalation-one-shot-semantics](idle-skip-escalation-one-shot-semantics.md) — Idle-skip & escalation one-shot semantics · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, tests/test_escalation.sh, tests/test_idle_skip.sh
- [jcode-event-stream-utilities](jcode-event-stream-utilities.md) — jcode Event Stream Utilities · scripts/core/engine-usage-cost.py, scripts/core/jcode-final-text.py
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — Jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-decision-browser-extraction](ki-k-decision-browser-extraction.md) — KİK Decision & Browser Extraction · scripts/ops/browse-extract.py, scripts/ops/kik-decision-read.py
- [linear-workstream-discipline](linear-workstream-discipline.md) — Linear Workstream Discipline · scripts/ops/linear-track.py
- [loop-lifecycle-monitoring](loop-lifecycle-monitoring.md) — Loop Lifecycle & Monitoring · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh
- [mcp-configuration-boot-probe](mcp-configuration-boot-probe.md) — MCP Configuration & Boot Probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-configuration-key-security](mcp-configuration-key-security.md) — MCP configuration & key security · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [operator-escalation-notification](operator-escalation-notification.md) — Operator Escalation & Notification · scripts/core/operator_request_notify.py, scripts/ops/operator-action-router.py
- [operator-request-decision-resolution](operator-request-decision-resolution.md) — Operator request & decision resolution · scripts/core/operator_request_notify.py, scripts/ops/operator-action-router.py, tests/test_operator_action_router.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [operator-usage-graft-refresh](operator-usage-graft-refresh.md) — Operator Usage & Graft Refresh · scripts/graft-auto-refresh.py, scripts/ops/operator-usage-report.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [opportunity-analyst-orchestration](opportunity-analyst-orchestration.md) — Opportunity Analyst Orchestration · scripts/ops/opportunity-analyst-cron.sh
- [ops-script-test-harness](ops-script-test-harness.md) — ops-script-test-harness · tests/test_reply_watch.sh, tests/test_send_gate.sh, tests/test_state_snapshot.sh, tests/test_tier_ladder_daily.sh, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [outreach-eligibility-evidence](outreach-eligibility-evidence.md) — Outreach Eligibility & Evidence · scripts/ops/g4-check.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [platform-status-scripts](platform-status-scripts.md) — Platform Status Scripts · scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [prompt-assembly-guardrails](prompt-assembly-guardrails.md) — Prompt assembly guardrails · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh
- [prompt-transport-contract](prompt-transport-contract.md) — Prompt transport contract · scripts/core/auto-loop.sh, tests/test_prompt_transport.sh
- [registry-evidence-maintenance](registry-evidence-maintenance.md) — Registry & Evidence Maintenance · scripts/ops/extract-axis-evidence.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [registry-queue-watchers](registry-queue-watchers.md) — Registry & queue watchers · scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [reply-watch](reply-watch.md) — reply-watch · scripts/ops/reply-watch.py, tests/test_reply_watch.sh
- [secret-handling-redaction](secret-handling-redaction.md) — Secret Handling & Redaction · scripts/core/jcode-mcp-config.py, scripts/core/operator_request_notify.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh
- [send-gate](send-gate.md) — send-gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-directive-writer](session-brief-directive-writer.md) — Session brief & directive writer · scripts/core/directive_writer.py, scripts/session-brief.py, tests/test_directive_section_refs.sh
- [set-e-shape-lint](set-e-shape-lint.md) — set-e-shape-lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/src/dashboard/pages.ts, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG Smoke Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [state-snapshot](state-snapshot.md) — state-snapshot · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [state-snapshot-probe](state-snapshot-probe.md) — State snapshot probe · scripts/ops/state-snapshot.py
- [telegram-notification-channel](telegram-notification-channel.md) — Telegram Notification Channel · scripts/core/telegram-notify.sh, scripts/ops/docker-prune-safe.sh
- [tool-usage-audit](tool-usage-audit.md) — tool-usage-audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [tool-usage-cost-analytics](tool-usage-cost-analytics.md) — Tool usage & cost analytics · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [turn-audit](turn-audit.md) — turn-audit · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [turn-economy-compliance-checks](turn-economy-compliance-checks.md) — Turn-Economy & Compliance Checks · scripts/ops/bloat-trend.py, scripts/ops/context7-check.py, scripts/ops/g4-check.py
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

65 per-file wiring cards mirror the source tree under `graft/` (63 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
