# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-read-write-guards](airtable-read-write-guards.md) — airtable-read-write-guards · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [analyst-engine](analyst-engine.md) — analyst-engine · scripts/analyst/opportunity-analyst-jcode.sh, tests/test_analyst_engine.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core](auto-loop-core.md) — auto-loop-core · scripts/core/auto-loop.sh, scripts/core/codex-final-text.py, scripts/core/directive_writer.py, scripts/core/engine-usage-cost.py, scripts/core/operator_request_notify.py, tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh, tests/test_directive_section_refs.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh, tests/test_operator_action_router.py, tests/test_operator_request_notify.py, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh
- [auto-loop-daemon](auto-loop-daemon.md) — Auto Loop Daemon · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [browse-extract-and-context7](browse-extract-and-context7.md) — browse-extract-and-context7 · scripts/ops/browse-extract.py, scripts/ops/context7-check.py, tests/test_browse_extract.sh, tests/test_context7_check.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py
- [cockpit-dashboard-server](cockpit-dashboard-server.md) — Cockpit Dashboard Server · dashboard/server.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-Hash Provenance · scripts/core/decision_text_hash.py
- [context-compact-hooks](context-compact-hooks.md) — Context & Compact Hooks · scripts/compact-preflight.py, scripts/context-watch.py
- [cycle-ndjson-log-format](cycle-ndjson-log-format.md) — cycle-ndjson-log-format · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py, tests/test_cost_model_hint.sh
- [dashboard-server](dashboard-server.md) — dashboard-server · dashboard/server.py, tests/test_dashboard_server.py, tests/test_refusal_format.sh
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [fail-closed-send-policy](fail-closed-send-policy.md) — Fail-closed send policy · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [g4-and-registry-matching](g4-and-registry-matching.md) — g4-and-registry-matching · scripts/ops/g4-check.py, tests/test_g4_check.sh
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [mcp-key-and-config-management](mcp-key-and-config-management.md) — mcp-key-and-config-management · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [north-star-metric-sql](north-star-metric-sql.md) — North-Star Metric SQL · docs/operations/north-star-metric-query.sql
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [ops-audit-and-telemetry-scripts](ops-audit-and-telemetry-scripts.md) — ops-audit-and-telemetry-scripts · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [outreach-ops-scripts](outreach-ops-scripts.md) — Outreach ops scripts · scripts/ops/reply-watch.py, scripts/ops/send-gate.py, scripts/ops/state-snapshot.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [outreach-ops-test-suites](outreach-ops-test-suites.md) — Outreach ops test suites · tests/test_reply_watch.sh, tests/test_send_gate.sh, tests/test_state_snapshot.sh, tests/test_tool_usage_audit.sh, tests/test_turn_audit.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod-mechanism-guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [registry-and-queue-ops](registry-and-queue-ops.md) — registry-and-queue-ops · scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [reply-silence-classification](reply-silence-classification.md) — Reply/silence classification · scripts/ops/reply-watch.py, tests/test_reply_watch.sh
- [scripts-core](scripts-core.md) — scripts/core · scripts/core/engine-usage-cost.py, scripts/core/jcode-final-text.py, scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/core/monitor.sh, scripts/core/operator_request_notify.py, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh, scripts/core/telegram-notify.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-hook](session-brief-hook.md) — session-brief-hook · scripts/session-brief.py
- [set-e-and-list-lint](set-e-and-list-lint.md) — set -e AND-list lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard](snapog-landing-dashboard.md) — SnapOG Landing & Dashboard · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-sample-scripts](snapog-sample-scripts.md) — SnapOG Sample Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot-delta](state-snapshot-delta.md) — State snapshot DELTA · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [tier-ladder-tests](tier-ladder-tests.md) — Tier ladder tests · tests/test_tier_ladder_daily.sh
- [tool-usage-audit](tool-usage-audit.md) — Tool usage audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-economy-policy](turn-economy-policy.md) — Turn economy policy · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [waitlist-function](waitlist-function.md) — Waitlist Function · projects/_archive/snapog-landing/functions/api/waitlist.ts
- [wsl-daemon-management](wsl-daemon-management.md) — wsl-daemon-management · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

65 per-file wiring cards mirror the source tree under `graft/` (63 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
