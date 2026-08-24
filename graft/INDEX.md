# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-ops](airtable-ops.md) — Airtable Ops · tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [analyst-engine](analyst-engine.md) — Analyst Engine · tests/test_analyst_engine.sh
- [analyst-skill-tooling](analyst-skill-tooling.md) — Analyst skill tooling · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/jcode-pilot-smoke.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-company site functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core](auto-loop-core.md) — Auto-Loop Core · scripts/core/auto-loop.sh, tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cycle_metadata.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous loop · scripts/core/auto-loop.sh
- [budget-spend-accounting](budget-spend-accounting.md) — Budget & Spend Accounting · tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_discretionary_budget.sh, tests/test_tier_ladder_daily.sh
- [cockpit-dashboard-server](cockpit-dashboard-server.md) — Cockpit dashboard server · dashboard/server.py
- [cockpit-dashboard-ui](cockpit-dashboard-ui.md) — Cockpit dashboard UI · dashboard/app.js
- [compact-preflight](compact-preflight.md) — Compact preflight · scripts/compact-preflight.py
- [container-entrypoint](container-entrypoint.md) — Container entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-hash provenance · scripts/core/decision_text_hash.py
- [context-watch-hook](context-watch-hook.md) — Context-watch hook · scripts/context-watch.py
- [cost-accounting-adapter](cost-accounting-adapter.md) — Cost accounting adapter · scripts/core/engine-usage-cost.py
- [cost-model-hint](cost-model-hint.md) — Cost Model Hint · tests/test_cost_model_hint.sh
- [dashboard-server](dashboard-server.md) — Dashboard Server · tests/test_dashboard_server.py, tests/test_refusal_format.sh
- [directive-writer](directive-writer.md) — Directive writer · scripts/core/directive_writer.py, tests/test_directive_section_refs.sh
- [engine-adapters](engine-adapters.md) — Engine Adapters · tests/test_cost_model_hint.sh, tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh, tests/test_prompt_transport.sh
- [fail-closed-measurement](fail-closed-measurement.md) — Fail-Closed Measurement · tests/test_ccusage_failclosed.sh, tests/test_jcode_mcp_config.sh, tests/test_mcp_probe.sh, tests/test_send_gate.sh
- [headinspect-header-inspector](headinspect-header-inspector.md) — HeadInspect header inspector · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idle-skip](idle-skip.md) — Idle Skip · tests/test_idle_skip.sh
- [mcp-configuration](mcp-configuration.md) — MCP Configuration · tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [mcp-probe](mcp-probe.md) — MCP Probe · tests/fixtures/mock_mcp_server.py, tests/test_mcp_probe.sh
- [operator-escalation](operator-escalation.md) — Operator Escalation · tests/test_escalation.sh
- [opportunity-analyst-pipeline](opportunity-analyst-pipeline.md) — Opportunity analyst pipeline · scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh
- [ops-scripts](ops-scripts.md) — Ops Scripts · tests/test_browse_extract.sh, tests/test_context7_check.sh, tests/test_g4_check.sh, tests/test_operator_request_notify.py, tests/test_refusal_format.sh, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh, tests/test_send_gate.sh, tests/test_state_snapshot.sh, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-Mechanism Guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [promotion-gate](promotion-gate.md) — Promotion gate · scripts/analyst/promote_directive.py
- [registry-merge-tool](registry-merge-tool.md) — Registry merge tool · scripts/analyst/merge_registry.py
- [sentry-reporter](sentry-reporter.md) — Sentry reporter · dashboard/sentry_client.py
- [session-brief](session-brief.md) — Session Brief · scripts/session-brief.py
- [session-leak-scanner](session-leak-scanner.md) — Session-leak scanner · scripts/core/bridge_leak_scan.py
- [set-e-safety](set-e-safety.md) — set -e Safety · tests/test_prompt_assembly.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerting](snapog-cost-alerting.md) — SnapOG cost alerting · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-og-image-service](snapog-og-image-service.md) — SnapOG OG image service · projects/_archive/snapog/src/dashboard/pages.ts, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-schema-waitlist](snapog-schema-waitlist.md) — SnapOG schema & waitlist · docs/operations/north-star-metric-query.sql, projects/_archive/snapog-landing/functions/api/waitlist.ts, projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG smoke tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [test-by-extraction](test-by-extraction.md) — Test-by-Extraction · tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_cycle_metadata.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_seteshape_lint.py, tests/test_tier_ladder_daily.sh
- [wsl-daemon-management](wsl-daemon-management.md) — WSL Daemon Management · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

61 per-file wiring cards mirror the source tree under `graft/` (59 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
