# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-bridge-access](airtable-bridge-access.md) — Airtable Bridge Access · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [auto-company-loop-orchestration](auto-company-loop-orchestration.md) — Auto Company Loop Orchestration · scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [auto-company-site-pages-functions](auto-company-site-pages-functions.md) — Auto-Company Site Pages Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-engine](auto-loop-core-engine.md) — auto-loop core engine · tests/test_cycle_metadata.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [auto-loop-orchestrator](auto-loop-orchestrator.md) — Auto Loop Orchestrator · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [compact-ritual-tooling](compact-ritual-tooling.md) — Compact Ritual Tooling · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [compliance-audit-watchers](compliance-audit-watchers.md) — Compliance & Audit Watchers · scripts/ops/bloat-trend.py, scripts/ops/budget-calibration-report.py, scripts/ops/context7-check.py, scripts/ops/cost-audit.py
- [consensus-memory-maintenance](consensus-memory-maintenance.md) — Consensus & Memory Maintenance · scripts/ops/consensus-prune.py, scripts/ops/idle-skip-note.py, scripts/ops/ledger-guard.py, scripts/ops/registry-archive.py
- [container-entrypoint-state-persistence](container-entrypoint-state-persistence.md) — Container Entrypoint & State Persistence · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-Hash Provenance · scripts/core/decision_text_hash.py, scripts/ops/kik-decision-read.py
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [cycle-metadata-extraction](cycle-metadata-extraction.md) — cycle metadata extraction · tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-server](dashboard-server.md) — dashboard server · tests/test_dashboard_server.py
- [directive-section-refs](directive-section-refs.md) — directive section refs · tests/test_directive_section_refs.sh
- [directive-writer-gate](directive-writer-gate.md) — Directive Writer Gate · dashboard/server.py, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [engine-output-extraction](engine-output-extraction.md) — Engine Output Extraction · scripts/core/codex-final-text.py, scripts/core/engine-usage-cost.py, scripts/core/jcode-final-text.py
- [escalation-one-shot-logic](escalation-one-shot-logic.md) — escalation one-shot logic · tests/test_escalation.sh
- [g4-gate](g4-gate.md) — G4 gate · tests/test_g4_check.sh, tests/test_send_gate.sh
- [graft-card-refresh](graft-card-refresh.md) — Graft Card Refresh · scripts/graft-auto-refresh.py
- [headinspect-header-inspector](headinspect-header-inspector.md) — HeadInspect Header Inspector · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [human-directive-lifecycle](human-directive-lifecycle.md) — Human Directive Lifecycle · scripts/core/directive_writer.py, scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [infrastructure-ops-guards](infrastructure-ops-guards.md) — Infrastructure & Ops Guards · scripts/core/sentry-heartbeat.sh, scripts/ops/docker-prune-safe.sh, scripts/ops/operator-usage-report.sh, scripts/ops/opportunity-analyst-cron.sh
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-registry-evidence](ki-k-registry-evidence.md) — KİK & Registry Evidence · scripts/ops/extract-axis-evidence.py, scripts/ops/g4-check.py, scripts/ops/kik-decision-read.py
- [ledger-guard](ledger-guard.md) — ledger guard · tests/test_ledger_guard.py
- [mcp-boot-compliance](mcp-boot-compliance.md) — MCP Boot & Compliance · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-config-generation-and-manifest-sync](mcp-config-generation-and-manifest-sync.md) — MCP config generation and manifest sync · tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh
- [mcp-probe](mcp-probe.md) — MCP probe · tests/test_mcp_probe.sh
- [operator-action-router](operator-action-router.md) — operator action router · tests/test_operator_action_router.py
- [operator-escalation-notification](operator-escalation-notification.md) — Operator Escalation & Notification · scripts/core/operator_request_notify.py, scripts/core/telegram-notify.sh, scripts/ops/directive-staleness-watch.py, scripts/ops/operator-action-router.py
- [operator-request-notify](operator-request-notify.md) — operator request notify · tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst-pipeline](opportunity-analyst-pipeline.md) — Opportunity Analyst Pipeline · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod mechanism guard · tests/test_prod_mechanism_guard.sh
- [prompt-transport-contract](prompt-transport-contract.md) — prompt transport contract · tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh
- [refusal-format](refusal-format.md) — refusal format · tests/test_refusal_format.sh
- [registry-operations](registry-operations.md) — registry operations · tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [reply-watch](reply-watch.md) — reply watch · tests/test_reply_watch.sh
- [rfq-operations](rfq-operations.md) — RFQ operations · tests/test_rfq_reply_watch.sh, tests/test_rfq_send.sh
- [runtime-env-secret-handling](runtime-env-secret-handling.md) — Runtime Env & Secret Handling · scripts/core/telegram-notify.sh, scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh, scripts/ops/operator-action-router.py, scripts/ops/operator-usage-report.sh, scripts/ops/registry-queue-watch.py
- [send-gate](send-gate.md) — send gate · tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [set-e-fatal-shape-lint](set-e-fatal-shape-lint.md) — set -e fatal shape lint · tests/test_prompt_assembly.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerting](snapog-cost-alerting.md) — SnapOG Cost Alerting · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql, projects/_archive/snapog/migrations/0001_init.sql
- [snapog-og-image-service](snapog-og-image-service.md) — SnapOG OG Image Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/dashboard/pages.ts, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG Smoke Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [spending-controls](spending-controls.md) — spending controls · tests/test_discretionary_budget.sh, tests/test_idle_skip.sh
- [state-snapshot](state-snapshot.md) — state snapshot · tests/test_state_snapshot.sh
- [tier-ladder-budget-selection](tier-ladder-budget-selection.md) — tier ladder budget selection · tests/test_tier_ladder_daily.sh
- [tool-usage-audit](tool-usage-audit.md) — tool usage audit · tests/test_tool_usage_audit.sh
- [turn-economy-policy](turn-economy-policy.md) — turn economy policy · tests/test_turn_audit.sh, tests/test_turn_bloat_brake.py
- [work-window-brake](work-window-brake.md) — work window brake · tests/test_work_window_watchdog.py, tests/test_work_window.py
- [workstream-queue-discipline](workstream-queue-discipline.md) — Workstream & Queue Discipline · scripts/ops/linear-track.py, scripts/ops/registry-queue-watch.py
- [wowcar-revenue-vocabulary](wowcar-revenue-vocabulary.md) — wowcar revenue vocabulary · tests/test_wowcar_revenue_vocabulary_acceptance.sh

## Files

86 per-file wiring cards mirror the source tree under `graft/` (84 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
