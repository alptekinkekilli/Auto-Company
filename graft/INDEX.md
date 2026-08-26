# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-wrappers](airtable-access-wrappers.md) — Airtable access wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [airtable-queue-watchers](airtable-queue-watchers.md) — Airtable Queue Watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [airtable-read-write-wrappers](airtable-read-write-wrappers.md) — Airtable Read/Write Wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [analyst-engine](analyst-engine.md) — Analyst engine · scripts/analyst/opportunity-analyst-jcode.sh
- [atomic-state-writes](atomic-state-writes.md) — Atomic State Writes · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/core/operator_request_notify.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-engine](auto-loop-core-engine.md) — Auto-loop core engine · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [budget-and-spend-accounting](budget-and-spend-accounting.md) — Budget and spend accounting · scripts/core/auto-loop.sh, scripts/ops/web-research-cost.py
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/server.py
- [compact-preflight](compact-preflight.md) — Compact Preflight · scripts/compact-preflight.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [context7-and-g4-checks](context7-and-g4-checks.md) — Context7 and g4 checks · scripts/ops/context7-check.py, scripts/ops/g4-check.py
- [context7-docs-cli](context7-docs-cli.md) — Context7 Docs CLI · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
- [core-bash-scripts](core-bash-scripts.md) — core bash scripts · tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [cost-budget-ledger-adapters](cost-budget-ledger-adapters.md) — Cost & Budget Ledger Adapters · scripts/core/engine-usage-cost.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py
- [directive-rule-compliance-watchers](directive-rule-compliance-watchers.md) — Directive & Rule Compliance Watchers · scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [engine-final-text-extractors](engine-final-text-extractors.md) — Engine Final-Text Extractors · scripts/core/codex-final-text.py
- [fail-closed-measurement](fail-closed-measurement.md) — Fail-closed measurement · scripts/core/auto-loop.sh, scripts/ops/state-snapshot.py, scripts/ops/verify-mcp-keys.py
- [fail-closed-verification-invariant](fail-closed-verification-invariant.md) — Fail-Closed Verification Invariant · scripts/ops/directive-rule-sweep.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [headinspect-inspection-logic](headinspect-inspection-logic.md) — HeadInspect Inspection Logic · projects/headinspect/src/inspect.ts
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idle-skip-and-escalation](idle-skip-and-escalation.md) — Idle-skip and escalation · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py
- [jcode-event-stream-utilities](jcode-event-stream-utilities.md) — jcode Event Stream Utilities · scripts/core/engine-usage-cost.py, scripts/core/jcode-final-text.py
- [jcode-mcp-config](jcode-mcp-config.md) — jcode MCP Config · scripts/core/jcode-mcp-config.py
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-decision-browser-extraction](ki-k-decision-browser-extraction.md) — KİK Decision & Browser Extraction · scripts/ops/browse-extract.py, scripts/ops/kik-decision-read.py
- [ki-k-decision-content-hash](ki-k-decision-content-hash.md) — KİK Decision Content Hash · scripts/core/decision_text_hash.py
- [linear-workstream-discipline](linear-workstream-discipline.md) — Linear Workstream Discipline · scripts/ops/linear-track.py
- [loop-lifecycle-monitoring](loop-lifecycle-monitoring.md) — Loop Lifecycle & Monitoring · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh
- [mcp-configuration-and-key-security](mcp-configuration-and-key-security.md) — MCP configuration and key security · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py
- [mcp-configuration-boot-probe](mcp-configuration-boot-probe.md) — MCP Configuration & Boot Probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-probe](mcp-probe.md) — MCP probe · scripts/core/jcode-mcp-probe.py, tests/fixtures/mock_mcp_server.py
- [offline-stubbing-test-pattern](offline-stubbing-test-pattern.md) — offline stubbing test pattern · tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh, tests/test_send_gate.sh, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [og-rendering](og-rendering.md) — OG Rendering · projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts
- [operator-escalation-notification](operator-escalation-notification.md) — Operator Escalation & Notification · scripts/core/operator_request_notify.py, scripts/ops/operator-action-router.py
- [operator-request-and-decision-ledger](operator-request-and-decision-ledger.md) — Operator request and decision ledger · scripts/core/operator_request_notify.py, scripts/ops/operator-action-router.py
- [operator-request-ledger](operator-request-ledger.md) — Operator Request Ledger · dashboard/server.py
- [operator-usage-graft-refresh](operator-usage-graft-refresh.md) — Operator Usage & Graft Refresh · scripts/graft-auto-refresh.py, scripts/ops/operator-usage-report.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/opportunity-analyst.sh
- [opportunity-analyst-jcode](opportunity-analyst-jcode.md) — Opportunity Analyst (jcode) · scripts/analyst/opportunity-analyst-jcode.sh
- [opportunity-analyst-orchestration](opportunity-analyst-orchestration.md) — Opportunity Analyst Orchestration · scripts/ops/opportunity-analyst-cron.sh
- [ops-audit-tooling](ops-audit-tooling.md) — Ops audit tooling · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [ops-watchers-audit-scripts](ops-watchers-audit-scripts.md) — ops watchers & audit scripts · tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh, tests/test_send_gate.sh, tests/test_state_snapshot.sh, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [outreach-eligibility-evidence](outreach-eligibility-evidence.md) — Outreach Eligibility & Evidence · scripts/ops/g4-check.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [platform-status-scripts](platform-status-scripts.md) — Platform Status Scripts · scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-mechanism guard · scripts/prod-mechanism-guard.py
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [prompt-transport-contract](prompt-transport-contract.md) — Prompt transport contract · scripts/core/auto-loop.sh
- [registry-and-browse-tooling](registry-and-browse-tooling.md) — Registry and browse tooling · scripts/ops/browse-extract.py, scripts/ops/registry-archive.py
- [registry-evidence-maintenance](registry-evidence-maintenance.md) — Registry & Evidence Maintenance · scripts/ops/extract-axis-evidence.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [secret-handling-redaction](secret-handling-redaction.md) — Secret Handling & Redaction · scripts/core/jcode-mcp-config.py, scripts/core/operator_request_notify.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh
- [secret-hygiene](secret-hygiene.md) — Secret hygiene · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py
- [send-gate-refusal-policy](send-gate-refusal-policy.md) — send-gate refusal policy · tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-and-directive-writer](session-brief-and-directive-writer.md) — Session brief and directive writer · scripts/core/directive_writer.py, scripts/session-brief.py
- [set-e-lint-app-240](set-e-lint-app-240.md) — set -e lint (APP-240) · tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard-pages](snapog-landing-dashboard-pages.md) — SnapOG Landing & Dashboard Pages · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric-sql](snapog-north-star-metric-sql.md) — SnapOG North-Star Metric SQL · docs/operations/north-star-metric-query.sql
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG Smoke Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-waitlist-function](snapog-waitlist-function.md) — SnapOG Waitlist Function
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/types.ts
- [state-persistence-idempotence](state-persistence-idempotence.md) — state persistence & idempotence · tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh, tests/test_tool_usage_audit.sh
- [state-snapshot-probe](state-snapshot-probe.md) — State snapshot probe · scripts/ops/state-snapshot.py
- [telegram-notification-channel](telegram-notification-channel.md) — Telegram Notification Channel · scripts/core/telegram-notify.sh, scripts/ops/docker-prune-safe.sh
- [tier-ladder-selection](tier-ladder-selection.md) — tier ladder selection · tests/test_tier_ladder_daily.sh
- [turn-economy-compliance-checks](turn-economy-compliance-checks.md) — Turn-Economy & Compliance Checks · scripts/ops/bloat-trend.py, scripts/ops/context7-check.py, scripts/ops/g4-check.py
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

65 per-file wiring cards mirror the source tree under `graft/` (63 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
