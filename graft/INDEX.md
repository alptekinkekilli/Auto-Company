# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-read-write-guards](airtable-read-write-guards.md) — Airtable read/write guards · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — auto-loop · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_tier_ladder_daily.sh
- [auto-loop-core](auto-loop-core.md) — Auto-loop core · scripts/core/auto-loop.sh, scripts/core/codex-final-text.py, scripts/core/directive_writer.py, scripts/core/engine-usage-cost.py, scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/core/operator_request_notify.py
- [claude-code-hooks-pretooluse-sessionstart](claude-code-hooks-pretooluse-sessionstart.md) — Claude Code hooks (PreToolUse/SessionStart) · scripts/prod-mechanism-guard.py, scripts/session-brief.py
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [compact-ritual](compact-ritual.md) — Compact Ritual · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py
- [compact-ritual-scripts](compact-ritual-scripts.md) — Compact ritual scripts · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py
- [container-bootstrap](container-bootstrap.md) — Container Bootstrap · docker-entrypoint.sh
- [context-watch](context-watch.md) — Context Watch · scripts/context-watch.py
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py
- [directive-writer](directive-writer.md) — Directive Writer · dashboard/server.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [fail-closed-measurement-invariant](fail-closed-measurement-invariant.md) — Fail-closed measurement invariant · scripts/core/auto-loop.sh, scripts/core/engine-usage-cost.py, scripts/ops/site-contact-evidence.py, tests/test_ccusage_failclosed.sh, tests/test_cost_model_hint.sh
- [g4-attribution-contact-evidence](g4-attribution-contact-evidence.md) — G4 attribution & contact evidence · scripts/ops/g4-check.py, scripts/ops/site-contact-evidence.py
- [headinspect-service](headinspect-service.md) — HeadInspect Service · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [loop-driver](loop-driver.md) — Loop Driver · scripts/core/auto-loop.sh, scripts/core/codex-final-text.py
- [mcp-config-key-handling](mcp-config-key-handling.md) — MCP config & key handling · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py
- [operator-decision-panel](operator-decision-panel.md) — operator-decision-panel · dashboard/server.py, scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [operator-request-action-routing](operator-request-action-routing.md) — Operator request & action routing · scripts/core/operator_request_notify.py, scripts/ops/operator-action-router.py
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [ops-probe-audit-scripts](ops-probe-audit-scripts.md) — Ops probe & audit scripts · scripts/ops/site-contact-evidence.py, scripts/ops/state-snapshot.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/verify-mcp-keys.py, scripts/ops/web-research-cost.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod-mechanism-guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [prompt-transport-contract](prompt-transport-contract.md) — prompt-transport-contract · scripts/core/auto-loop.sh, tests/test_prompt_transport.sh
- [registry-archive](registry-archive.md) — registry-archive · scripts/ops/registry-archive.py, tests/test_registry_archive.sh
- [registry-merge-invariants](registry-merge-invariants.md) — Registry Merge Invariants · scripts/analyst/merge_registry.py
- [registry-queue-watch](registry-queue-watch.md) — registry-queue-watch · scripts/ops/registry-queue-watch.py, tests/test_registry_queue_watch.sh
- [reply-watch](reply-watch.md) — reply-watch · scripts/ops/reply-watch.py, tests/test_reply_watch.sh
- [secrets-never-in-argv](secrets-never-in-argv.md) — Secrets never in argv · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [send-gate](send-gate.md) — send-gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [set-e-shape-lint](set-e-shape-lint.md) — set-e-shape-lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard](snapog-landing-dashboard.md) — SnapOG Landing/Dashboard · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-sample-tests](snapog-sample-tests.md) — SnapOG Sample Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot](state-snapshot.md) — state-snapshot · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [test-extraction-strategy](test-extraction-strategy.md) — Test extraction strategy · tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_cycle_counter.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh
- [test-suite-for-auto-loop-core](test-suite-for-auto-loop-core.md) — Test suite for auto-loop core · tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh
- [test-suite-for-mcp-config-probe](test-suite-for-mcp-config-probe.md) — Test suite for MCP config & probe · tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [test-suite-for-ops-scripts](test-suite-for-ops-scripts.md) — Test suite for ops scripts · tests/test_airtable_read.sh, tests/test_airtable_write.sh, tests/test_browse_extract.sh, tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh, tests/test_context7_check.sh, tests/test_cost_model_hint.sh, tests/test_dashboard_server.py, tests/test_directive_section_refs.sh, tests/test_g4_check.sh, tests/test_operator_action_router.py, tests/test_operator_request_notify.py
- [tool-usage-audit](tool-usage-audit.md) — tool-usage-audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-economy](turn-economy.md) — turn-economy · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [value-sensitive-leak-scanner](value-sensitive-leak-scanner.md) — Value-Sensitive Leak Scanner · scripts/core/bridge_leak_scan.py
- [wowcar-revenue-relabel-acceptance-harness](wowcar-revenue-relabel-acceptance-harness.md) — Wowcar revenue relabel acceptance harness · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-vocabulary-acceptance](wowcar-vocabulary-acceptance.md) — wowcar-vocabulary-acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-systemd-daemon-scripts](wsl-systemd-daemon-scripts.md) — WSL systemd daemon scripts · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

69 per-file wiring cards mirror the source tree under `graft/` (67 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
