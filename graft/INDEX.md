# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-ops-watchers](airtable-ops-watchers.md) — Airtable ops watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py
- [airtable-read-wrapper](airtable-read-wrapper.md) — Airtable read wrapper · scripts/ops/airtable-read.py
- [airtable-write-guard](airtable-write-guard.md) — Airtable write guard · scripts/ops/airtable-write.py
- [analyst-engine](analyst-engine.md) — Analyst engine · scripts/analyst/opportunity-analyst-jcode.sh
- [analyst-tooling](analyst-tooling.md) — Analyst Tooling · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/jcode-pilot-smoke.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-engine](auto-loop-core-engine.md) — auto-loop core engine · scripts/core/auto-loop.sh
- [auto-loop-daemon](auto-loop-daemon.md) — Auto Loop Daemon · scripts/core/auto-loop.sh
- [auto-loop-harness](auto-loop-harness.md) — Auto-loop harness · scripts/core/auto-loop.sh, scripts/ops/ledger-guard.py, scripts/ops/state-snapshot.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/turn-bloat-brake.py, scripts/ops/verify-mcp-keys.py, scripts/ops/web-research-cost.py, scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py
- [budget-gates](budget-gates.md) — Budget gates · scripts/core/auto-loop.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py
- [cockpit-server](cockpit-server.md) — Cockpit Server · dashboard/server.py
- [compact-path-canonicalization](compact-path-canonicalization.md) — Compact Path Canonicalization · scripts/compact_yol.py
- [compact-ritual](compact-ritual.md) — Compact ritual · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py, scripts/session-brief.py
- [compact-ritual-hooks](compact-ritual-hooks.md) — Compact Ritual Hooks · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [cost-model-hint](cost-model-hint.md) — Cost model hint · scripts/core/auto-loop.sh
- [dashboard-server](dashboard-server.md) — dashboard server · dashboard/server.py, tests/test_dashboard_server.py
- [directive-writer](directive-writer.md) — Directive Writer · dashboard/server.py, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py, scripts/core/directive_writer.py, tests/test_directive_section_refs.sh
- [discretionary-budget-cap](discretionary-budget-cap.md) — discretionary budget cap · scripts/core/auto-loop.sh, tests/test_discretionary_budget.sh
- [escalation-one-shot-semantics](escalation-one-shot-semantics.md) — escalation one-shot semantics · scripts/core/auto-loop.sh, tests/test_escalation.sh
- [g4-check](g4-check.md) — g4 check · scripts/ops/g4-check.py, tests/test_g4_check.sh
- [headinspect-schema](headinspect-schema.md) — HeadInspect Schema · projects/headinspect/migrations/0001_hits.sql
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idle-skip-mechanism](idle-skip-mechanism.md) — idle-skip mechanism · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, tests/test_discretionary_budget.sh, tests/test_idle_skip.sh
- [ledger-guard](ledger-guard.md) — ledger guard · scripts/ops/ledger-guard.py, tests/test_ledger_guard.py
- [mcp-config-sync-invariant](mcp-config-sync-invariant.md) — MCP config sync invariant · scripts/core/auto-loop.sh, scripts/core/jcode-mcp-config.py, tests/test_mcp_config_manifest_sync.sh
- [mcp-key-fallback](mcp-key-fallback.md) — MCP key fallback · scripts/core/jcode-mcp-config.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [mcp-probe](mcp-probe.md) — MCP probe · scripts/core/jcode-mcp-probe.py, tests/fixtures/mock_mcp_server.py, tests/test_mcp_probe.sh
- [mcp-verification](mcp-verification.md) — MCP verification · scripts/ops/verify-mcp-keys.py
- [mixed-harness-attribution](mixed-harness-attribution.md) — mixed-harness attribution · scripts/core/auto-loop.sh, tests/test_mixed_harness.sh
- [mock-mcp-server-fixture](mock-mcp-server-fixture.md) — Mock MCP server fixture · tests/fixtures/mock_mcp_server.py
- [operator-action-router](operator-action-router.md) — operator action router · scripts/ops/operator-action-router.py, tests/test_operator_action_router.py
- [operator-request-notify](operator-request-notify.md) — operator request notify · scripts/core/operator_request_notify.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [outreach-eligibility-gate](outreach-eligibility-gate.md) — Outreach eligibility gate · scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [outreach-watchers](outreach-watchers.md) — outreach watchers · scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py, tests/test_reply_watch.sh, tests/test_rfq_reply_watch.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [prompt-assembly-guardrails](prompt-assembly-guardrails.md) — prompt assembly guardrails · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh
- [prompt-transport-contract](prompt-transport-contract.md) — prompt transport contract · scripts/core/auto-loop.sh, tests/test_prompt_transport.sh
- [refusal-format-contract](refusal-format-contract.md) — refusal format contract · dashboard/server.py, scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [registry-archive](registry-archive.md) — registry archive · scripts/ops/registry-archive.py, tests/test_registry_archive.sh
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [registry-queue-watch](registry-queue-watch.md) — registry queue watch · scripts/ops/registry-queue-watch.py, tests/test_registry_queue_watch.sh
- [rfq-send](rfq-send.md) — rfq send · scripts/ops/rfq-send.py, tests/test_rfq_send.sh
- [rfq-send-pipeline](rfq-send-pipeline.md) — RFQ send pipeline · scripts/ops/rfq_template.py, scripts/ops/rfq-reply-watch.py, scripts/ops/rfq-send.py
- [send-gate](send-gate.md) — send gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [set-e-shape-lint](set-e-shape-lint.md) — set -e shape lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard-pages](snapog-landing-dashboard-pages.md) — SnapOG Landing & Dashboard Pages · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG Smoke Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot](state-snapshot.md) — State snapshot · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [telegram-notify-shell-out](telegram-notify-shell-out.md) — Telegram notify shell-out · scripts/core/telegram-notify.sh
- [test-harnesses](test-harnesses.md) — Test harnesses · tests/test_active_window.sh, tests/test_airtable_read.sh, tests/test_airtable_write.sh, tests/test_analyst_engine.sh, tests/test_auto_loop_ledger_guard.sh, tests/test_auto_loop_work_window.sh, tests/test_browse_extract.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh, tests/test_compact_yol.py, tests/test_context7_check.sh, tests/test_cost_audit_tool_surface.py, tests/test_cost_model_hint.sh, tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh
- [tier-ladder-daily-budget](tier-ladder-daily-budget.md) — tier ladder daily budget · scripts/core/auto-loop.sh, tests/test_tier_ladder_daily.sh
- [tool-usage-audit](tool-usage-audit.md) — tool usage audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-bloat-brake](turn-bloat-brake.md) — turn bloat brake · scripts/ops/turn-bloat-brake.py, tests/test_turn_bloat_brake.py
- [turn-economy-audit](turn-economy-audit.md) — turn economy audit · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [work-window-brake](work-window-brake.md) — Work-window brake · scripts/ops/state-snapshot.py, scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py, tests/test_work_window.py
- [work-window-watchdog](work-window-watchdog.md) — work window watchdog · scripts/ops/work-window-watchdog.py, tests/test_work_window_watchdog.py
- [wowcar-revenue-relabel-acceptance](wowcar-revenue-relabel-acceptance.md) — Wowcar revenue relabel acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary](wowcar-revenue-vocabulary.md) — wowcar revenue vocabulary · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-daemon](wsl-daemon.md) — WSL daemon · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

84 per-file wiring cards mirror the source tree under `graft/` (82 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
