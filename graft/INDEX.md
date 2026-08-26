# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-read-write-guards](airtable-read-write-guards.md) — Airtable read/write guards · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [airtable-read-write-wrappers](airtable-read-write-wrappers.md) — Airtable Read/Write Wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [analyst-final-text-extraction](analyst-final-text-extraction.md) — Analyst Final-Text Extraction · scripts/analyst/opportunity-analyst-jcode.sh, scripts/core/codex-final-text.py
- [analyst-tooling](analyst-tooling.md) — Analyst Tooling · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/jcode-pilot-smoke.sh
- [atomic-state-writes](atomic-state-writes.md) — Atomic State Writes · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/core/operator_request_notify.py, scripts/ops/directive-staleness-watch.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — Auto Loop · scripts/core/auto-loop.sh
- [auto-loop-core-engine](auto-loop-core-engine.md) — Auto-loop core engine · scripts/core/auto-loop.sh
- [auto-loop-sh](auto-loop-sh.md) — auto-loop.sh · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [browseros-browse-extract](browseros-browse-extract.md) — BrowserOS Browse & Extract · scripts/ops/browse-extract.py
- [budget-spend-accounting](budget-spend-accounting.md) — Budget & spend accounting · scripts/core/auto-loop.sh, scripts/core/engine-usage-cost.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cost_model_hint.sh, tests/test_mixed_harness.sh
- [business-hours-gate-off-hours-behavior](business-hours-gate-off-hours-behavior.md) — Business-hours gate & off-hours behavior · scripts/core/auto-loop.sh, tests/test_active_window.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py, tests/test_dashboard_server.py, tests/test_refusal_format.sh
- [compliance-audit-watchers](compliance-audit-watchers.md) — Compliance & Audit Watchers · scripts/ops/context7-check.py, scripts/ops/directive-rule-sweep.py, scripts/ops/extract-axis-evidence.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-Hash Provenance · scripts/core/decision_text_hash.py
- [context-monitoring-hooks](context-monitoring-hooks.md) — Context Monitoring Hooks · scripts/compact-preflight.py, scripts/context-watch.py
- [cost-budget-ledger-adapters](cost-budget-ledger-adapters.md) — Cost & Budget Ledger Adapters · scripts/core/engine-usage-cost.py, scripts/ops/bloat-trend.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py
- [cycle-metadata-extraction](cycle-metadata-extraction.md) — Cycle metadata extraction · scripts/core/auto-loop.sh, tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-server](dashboard-server.md) — Dashboard Server · dashboard/server.py
- [directive-promotion-gate](directive-promotion-gate.md) — Directive Promotion Gate · scripts/analyst/promote_directive.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [docker-entrypoint-sh](docker-entrypoint-sh.md) — docker-entrypoint.sh · docker-entrypoint.sh
- [escalation-operator-requests](escalation-operator-requests.md) — Escalation & operator requests · scripts/core/auto-loop.sh, scripts/core/operator_request_notify.py, tests/test_escalation.sh, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [external-ops-integrations](external-ops-integrations.md) — External Ops Integrations · scripts/ops/kik-decision-read.py, scripts/ops/linear-track.py, scripts/ops/operator-usage-report.sh
- [fail-closed-measurement-invariant](fail-closed-measurement-invariant.md) — Fail-closed measurement invariant · scripts/core/auto-loop.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_mixed_harness.sh
- [fail-closed-verification](fail-closed-verification.md) — Fail-Closed Verification · scripts/core/jcode-mcp-probe.py, scripts/ops/directive-rule-sweep.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py, scripts/ops/send-gate.py
- [g4-identity-attribution](g4-identity-attribution.md) — G4 Identity Attribution · scripts/ops/g4-check.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [g4-verification-registry-archive](g4-verification-registry-archive.md) — G4 verification & registry archive · scripts/ops/g4-check.py, scripts/ops/registry-archive.py, tests/test_g4_check.sh, tests/test_registry_archive.sh
- [graft-auto-refresh](graft-auto-refresh.md) — Graft Auto-Refresh · scripts/graft-auto-refresh.py
- [headinspect-schema](headinspect-schema.md) — HeadInspect Schema · projects/headinspect/migrations/0001_hits.sql
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idle-skip-discretionary-budget](idle-skip-discretionary-budget.md) — Idle-skip & discretionary budget · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, tests/test_discretionary_budget.sh, tests/test_idle_skip.sh
- [jcode-event-stream-utilities](jcode-event-stream-utilities.md) — jcode Event Stream Utilities · scripts/core/engine-usage-cost.py, scripts/core/jcode-final-text.py
- [loop-lifecycle-monitoring](loop-lifecycle-monitoring.md) — Loop Lifecycle & Monitoring · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh
- [mcp-boot-probe](mcp-boot-probe.md) — MCP Boot & Probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-configuration-key-security](mcp-configuration-key-security.md) — MCP configuration & key security · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [offline-testability-via-awk-extraction-stubbing](offline-testability-via-awk-extraction-stubbing.md) — Offline testability via awk extraction & stubbing · tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_escalation.sh, tests/test_mcp_key_fallback.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_send_gate.sh
- [operator-escalation-gate](operator-escalation-gate.md) — Operator Escalation Gate · scripts/core/operator_request_notify.py, scripts/ops/directive-staleness-watch.py, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh
- [opportunity-analyst-orchestration](opportunity-analyst-orchestration.md) — Opportunity Analyst Orchestration · scripts/ops/opportunity-analyst-cron.sh
- [ops-audit-analytics-scripts](ops-audit-analytics-scripts.md) — Ops audit & analytics scripts · scripts/ops/context7-check.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py, tests/test_context7_check.sh
- [ops-audit-ledger-idempotence-cycle-file-semantics](ops-audit-ledger-idempotence-cycle-file-semantics.md) — ops audit ledger idempotence & cycle-file semantics · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [outreach-eligibility-brake](outreach-eligibility-brake.md) — Outreach Eligibility Brake · scripts/ops/send-gate.py
- [outreach-send-gate](outreach-send-gate.md) — Outreach & send gate · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/send-gate.py, tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh, tests/test_send_gate.sh
- [platform-status-reports](platform-status-reports.md) — Platform Status Reports · scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [prompt-transport-assembly](prompt-transport-assembly.md) — Prompt transport & assembly · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh
- [registry-archive-state](registry-archive-state.md) — Registry Archive & State · scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [secret-handling](secret-handling.md) — Secret Handling · scripts/core/jcode-mcp-config.py, scripts/core/operator_request_notify.py, scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh
- [secret-hygiene-in-argv-vs-env](secret-hygiene-in-argv-vs-env.md) — Secret hygiene in argv vs env · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-directive-writer](session-brief-directive-writer.md) — Session brief & directive writer · scripts/core/directive_writer.py, scripts/session-brief.py, tests/test_directive_section_refs.sh
- [set-e-and-or-list-safety-invariant](set-e-and-or-list-safety-invariant.md) — set -e AND-OR list safety invariant · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [set-e-shape-lint-tests-test-seteshape-lint-py](set-e-shape-lint-tests-test-seteshape-lint-py.md) — set-e shape lint (tests/test_seteshape_lint.py) · tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-waitlist](snapog-landing-waitlist.md) — SnapOG Landing & Waitlist · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-og-rendering](snapog-og-rendering.md) — SnapOG OG Rendering · projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG Smoke Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot-ops-script-tests](state-snapshot-ops-script-tests.md) — state-snapshot ops script + tests · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [telegram-notification-channel](telegram-notification-channel.md) — Telegram Notification Channel · scripts/core/telegram-notify.sh, scripts/ops/docker-prune-safe.sh
- [threshold-recalibration-vs-measurement](threshold-recalibration-vs-measurement.md) — Threshold Recalibration vs Measurement · scripts/ops/bloat-trend.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py
- [tier-ladder-daily-tests](tier-ladder-daily-tests.md) — tier ladder daily tests · tests/test_tier_ladder_daily.sh
- [tool-usage-audit-ops-script-tests](tool-usage-audit-ops-script-tests.md) — tool-usage-audit ops script + tests · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-audit-ops-script-tests](turn-audit-ops-script-tests.md) — turn-audit ops script + tests · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [unknown-model-conservative-pricing](unknown-model-conservative-pricing.md) — Unknown-Model Conservative Pricing · scripts/core/engine-usage-cost.py, scripts/ops/cost-audit.py
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

63 per-file wiring cards mirror the source tree under `graft/` (61 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
