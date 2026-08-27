# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable](airtable.md) — airtable · tests/test_registry_queue_watch.sh, tests/test_reply_watch.sh, tests/test_send_gate.sh
- [airtable-access-wrapper](airtable-access-wrapper.md) — Airtable access wrapper · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/verify-mcp-keys.py
- [analyst-engine-runner](analyst-engine-runner.md) — Analyst engine runner · scripts/analyst/opportunity-analyst-jcode.sh
- [analyst-tooling](analyst-tooling.md) — Analyst Tooling · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/jcode-pilot-smoke.sh, scripts/core/bridge_leak_scan.py
- [audit-telemetry-tooling](audit-telemetry-tooling.md) — Audit & telemetry tooling · scripts/ops/context7-check.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — auto_loop · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_tier_ladder_daily.sh
- [auto-loop-core-auto-loop-sh](auto-loop-core-auto-loop-sh.md) — Auto-loop core (auto-loop.sh) · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [budget-spend-accounting](budget-spend-accounting.md) — Budget & spend accounting · scripts/core/auto-loop.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py
- [cockpit-server](cockpit-server.md) — Cockpit Server · dashboard/server.py
- [compact-ritual-directive-integrity](compact-ritual-directive-integrity.md) — Compact ritual & directive integrity · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py, scripts/core/directive_writer.py, tests/test_compact_anchor_sync.py
- [compact-ritual-hooks](compact-ritual-hooks.md) — Compact Ritual Hooks · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [context-watch](context-watch.md) — Context Watch · scripts/context-watch.py
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py, tests/test_refusal_format.sh
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [fail-closed-invariant](fail-closed-invariant.md) — Fail-closed invariant · scripts/analyst/opportunity-analyst-jcode.sh, scripts/core/auto-loop.sh, scripts/core/jcode-mcp-probe.py, scripts/ops/send-gate.py, scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [g4-attribution-contact-evidence](g4-attribution-contact-evidence.md) — G4 attribution & contact evidence · scripts/ops/g4-check.py, scripts/ops/site-contact-evidence.py
- [headinspect-inspection-logic](headinspect-inspection-logic.md) — HeadInspect Inspection Logic · projects/headinspect/src/inspect.ts
- [headinspect-renderer](headinspect-renderer.md) — HeadInspect Renderer · projects/headinspect/src/render.ts
- [headinspect-schema](headinspect-schema.md) — HeadInspect Schema · projects/headinspect/migrations/0001_hits.sql
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/src/index.ts
- [mcp-config-generation-probe](mcp-config-generation-probe.md) — MCP config generation & probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, tests/fixtures/mock_mcp_server.py
- [operator-escalation-routing](operator-escalation-routing.md) — Operator escalation & routing · scripts/core/auto-loop.sh, scripts/ops/operator-action-router.py
- [operator-request-notify](operator-request-notify.md) — operator_request_notify · scripts/core/operator_request_notify.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh
- [outreach-eligibility-gate-send-gate-py](outreach-eligibility-gate-send-gate-py.md) — Outreach eligibility gate (send-gate.py) · scripts/ops/send-gate.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod_mechanism_guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [prod-mechanism-guard-session-brief](prod-mechanism-guard-session-brief.md) — Prod-mechanism guard & session brief · scripts/prod-mechanism-guard.py, scripts/session-brief.py
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [prompt-transport](prompt-transport.md) — prompt_transport · scripts/core/auto-loop.sh, tests/test_prompt_transport.sh
- [refusal-format](refusal-format.md) — refusal_format · scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [registry-ops](registry-ops.md) — registry_ops · scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [reply-watch](reply-watch.md) — reply_watch · scripts/ops/reply-watch.py, tests/test_reply_watch.sh
- [secrets-never-in-argv](secrets-never-in-argv.md) — Secrets never in argv · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, tests/test_mcp_key_fallback.sh
- [send-gate](send-gate.md) — send_gate · scripts/ops/send-gate.py, tests/test_send_gate.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [set-e-lint](set-e-lint.md) — set_e_lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-waitlist](snapog-landing-waitlist.md) — SnapOG Landing & Waitlist · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-og-rendering](snapog-og-rendering.md) — SnapOG OG Rendering · projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts
- [snapog-schema](snapog-schema.md) — SnapOG Schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot](state-snapshot.md) — state_snapshot · scripts/ops/state-snapshot.py, tests/test_state_snapshot.sh
- [state-snapshot-idle-detection](state-snapshot-idle-detection.md) — State snapshot & idle detection · scripts/ops/idle-skip-note.py, scripts/ops/state-snapshot.py
- [test-by-extraction-strategy](test-by-extraction-strategy.md) — Test-by-extraction strategy · tests/test_airtable_write.sh, tests/test_budget_gates.sh, tests/test_cycle_counter.sh, tests/test_escalation.sh, tests/test_g4_check.sh
- [tool-usage-audit](tool-usage-audit.md) — tool_usage_audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-audit](turn-audit.md) — turn_audit · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [wowcar-revenue-relabel-acceptance](wowcar-revenue-relabel-acceptance.md) — Wowcar revenue relabel acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-vocabulary](wowcar-vocabulary.md) — wowcar_vocabulary · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

70 per-file wiring cards mirror the source tree under `graft/` (68 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
