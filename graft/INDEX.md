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
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core](auto-loop-core.md) — auto-loop core · scripts/core/auto-loop.sh, tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py, tests/test_dashboard_server.py
- [codex-final-text](codex-final-text.md) — Codex Final Text · scripts/core/codex-final-text.py
- [compact-preflight](compact-preflight.md) — Compact Preflight · scripts/compact-preflight.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-Hash Provenance · projects/_archive/snapog/src/og/render.ts, scripts/core/decision_text_hash.py
- [context-watch](context-watch.md) — Context Watch · scripts/context-watch.py
- [dashboard-server](dashboard-server.md) — Dashboard Server · dashboard/server.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [escalation-one-shot-consumption](escalation-one-shot-consumption.md) — escalation & one-shot consumption · scripts/core/auto-loop.sh, tests/test_escalation.sh
- [fail-closed-measurement-spend-accounting](fail-closed-measurement-spend-accounting.md) — fail-closed measurement & spend accounting · scripts/core/auto-loop.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh
- [fail-closed-send-policy](fail-closed-send-policy.md) — Fail-closed send policy · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [headinspect-schema](headinspect-schema.md) — HeadInspect Schema · projects/headinspect/migrations/0001_hits.sql
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idempotent-durable-ledgers](idempotent-durable-ledgers.md) — idempotent durable ledgers · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [mcp-config-key-management](mcp-config-key-management.md) — MCP config & key management · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [operator-request-decision-pipeline](operator-request-decision-pipeline.md) — operator request & decision pipeline · scripts/core/operator_request_notify.py, scripts/ops/operator-action-router.py, tests/test_operator_action_router.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [ops-analysis-audit-tools](ops-analysis-audit-tools.md) — ops analysis & audit tools · scripts/core/codex-final-text.py, scripts/core/directive_writer.py, scripts/core/engine-usage-cost.py, scripts/ops/browse-extract.py, scripts/ops/context7-check.py, scripts/ops/g4-check.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, tests/test_browse_extract.sh, tests/test_context7_check.sh, tests/test_cost_model_hint.sh, tests/test_directive_section_refs.sh, tests/test_g4_check.sh, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [ops-audit-analytics-scripts](ops-audit-analytics-scripts.md) — ops audit & analytics scripts · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [outreach-ops-scripts](outreach-ops-scripts.md) — Outreach ops scripts · scripts/ops/reply-watch.py, scripts/ops/send-gate.py, scripts/ops/state-snapshot.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [outreach-ops-test-suites](outreach-ops-test-suites.md) — Outreach ops test suites · tests/test_reply_watch.sh, tests/test_send_gate.sh, tests/test_state_snapshot.sh, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [production-mechanism-guard](production-mechanism-guard.md) — production mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [prompt-transport-assembly-safety](prompt-transport-assembly-safety.md) — prompt transport & assembly safety · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [reply-silence-classification](reply-silence-classification.md) — Reply/silence classification · scripts/ops/reply-watch.py, tests/test_reply_watch.sh
- [scripts-core](scripts-core.md) — scripts/core · scripts/core/engine-usage-cost.py, scripts/core/jcode-final-text.py, scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/core/monitor.sh, scripts/core/operator_request_notify.py, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh, scripts/core/telegram-notify.sh
- [secret-hygiene-in-argv-vs-env](secret-hygiene-in-argv-vs-env.md) — secret hygiene in argv vs env · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-hooks](session-brief-hooks.md) — session brief & hooks · scripts/session-brief.py
- [set-e-and-list-lint](set-e-and-list-lint.md) — set -e AND-list lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG Smoke Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/dashboard/pages.ts, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot-delta](state-snapshot-delta.md) — State snapshot DELTA · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [tier-ladder-tests](tier-ladder-tests.md) — Tier ladder tests · tests/test_tier_ladder_daily.sh
- [tool-usage-audit](tool-usage-audit.md) — Tool usage audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-economy-policy](turn-economy-policy.md) — Turn economy policy · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

65 per-file wiring cards mirror the source tree under `graft/` (63 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
