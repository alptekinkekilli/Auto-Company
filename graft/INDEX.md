# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-layer](airtable-access-layer.md) — Airtable access layer · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [airtable-read-write-guards](airtable-read-write-guards.md) — Airtable read/write guards · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [analyst-research-engines](analyst-research-engines.md) — analyst & research engines · scripts/analyst/opportunity-analyst-jcode.sh, scripts/ops/web-research-cost.py, tests/test_analyst_engine.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-loop](auto-loop-core-loop.md) — auto-loop core loop · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [browse-extract-harness](browse-extract-harness.md) — browse & extract harness · scripts/ops/browse-extract.py, scripts/ops/site-contact-evidence.py
- [budget-spend-accounting](budget-spend-accounting.md) — budget & spend accounting · scripts/core/auto-loop.sh, scripts/core/engine-usage-cost.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cost_model_hint.sh, tests/test_tier_ladder_daily.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js
- [cockpit-server](cockpit-server.md) — Cockpit Server · dashboard/server.py
- [compact-preflight](compact-preflight.md) — Compact Preflight · scripts/compact-preflight.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-canon](content-hash-canon.md) — Content Hash Canon · scripts/core/decision_text_hash.py
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [context7-docs-cli](context7-docs-cli.md) — Context7 Docs CLI · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
- [cost-accounting](cost-accounting.md) — Cost Accounting · scripts/core/engine-usage-cost.py
- [cost-budget-telemetry](cost-budget-telemetry.md) — cost & budget telemetry · scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py, scripts/ops/operator-usage-report.sh
- [cycle-ledger-idempotence-invariant](cycle-ledger-idempotence-invariant.md) — cycle ledger idempotence invariant · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [cycle-metadata-extraction](cycle-metadata-extraction.md) — cycle metadata extraction · scripts/core/auto-loop.sh, tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-cockpit](dashboard-cockpit.md) — dashboard & cockpit · dashboard/server.py, tests/test_dashboard_server.py, tests/test_refusal_format.sh
- [directive-rule-governance](directive-rule-governance.md) — directive & rule governance · scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [docker-disk-guard](docker-disk-guard.md) — Docker disk guard · scripts/ops/docker-prune-safe.sh
- [escalation-operator-requests](escalation-operator-requests.md) — escalation & operator requests · scripts/core/auto-loop.sh, scripts/core/operator_request_notify.py, tests/test_escalation.sh, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [evidence-extraction-compliance](evidence-extraction-compliance.md) — evidence extraction & compliance · scripts/ops/context7-check.py, scripts/ops/extract-axis-evidence.py, scripts/ops/idle-skip-note.py
- [fail-closed-fail-open-invariants](fail-closed-fail-open-invariants.md) — fail-closed & fail-open invariants · scripts/core/auto-loop.sh, scripts/core/jcode-mcp-config.py, scripts/ops/send-gate.py, scripts/prod-mechanism-guard.py, tests/test_active_window.sh, tests/test_ccusage_failclosed.sh, tests/test_idle_skip.sh, tests/test_send_gate.sh
- [graft-card-refresh](graft-card-refresh.md) — graft card refresh · scripts/graft-auto-refresh.py
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idle-skip-off-hours](idle-skip-off-hours.md) — idle-skip & off-hours · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, scripts/ops/state-snapshot.py, tests/test_active_window.sh, tests/test_discretionary_budget.sh, tests/test_idle_skip.sh, tests/test_state_snapshot.sh
- [jcode-event-stream-utilities](jcode-event-stream-utilities.md) — jcode event-stream utilities · scripts/core/jcode-final-text.py, scripts/ops/context7-check.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [jcode-mcp-boot-gate](jcode-mcp-boot-gate.md) — jcode MCP boot gate · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-procurement-digest](ki-k-procurement-digest.md) — KİK procurement digest · scripts/ops/kik-decision-read.py
- [linear-workstream-tracker](linear-workstream-tracker.md) — Linear workstream tracker · scripts/ops/linear-track.py
- [loop-lifecycle-monitoring](loop-lifecycle-monitoring.md) — loop lifecycle & monitoring · scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [mcp-config-key-handling](mcp-config-key-handling.md) — MCP config & key handling · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [og-rendering](og-rendering.md) — OG Rendering · projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts
- [operator-escalation-gate](operator-escalation-gate.md) — operator escalation gate · scripts/core/operator_request_notify.py
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — Opportunity Analyst cron · scripts/ops/opportunity-analyst-cron.sh
- [ops-scripts](ops-scripts.md) — ops scripts · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/browse-extract.py, scripts/ops/context7-check.py, scripts/ops/g4-check.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/send-gate.py, scripts/ops/state-snapshot.py, scripts/ops/verify-mcp-keys.py, scripts/ops/web-research-cost.py
- [outreach-eligibility-brake](outreach-eligibility-brake.md) — outreach eligibility brake · scripts/ops/g4-check.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [outreach-send-gate](outreach-send-gate.md) — outreach & send gate · scripts/ops/reply-watch.py, scripts/ops/send-gate.py, tests/test_reply_watch.sh, tests/test_send_gate.sh
- [outreach-watchers](outreach-watchers.md) — outreach watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — prod-mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [prompt-assembly-transport](prompt-assembly-transport.md) — prompt assembly & transport · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh
- [registry-archive-state-snapshot](registry-archive-state-snapshot.md) — registry archive & state snapshot · scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py
- [registry-merge](registry-merge.md) — Registry Merge · scripts/analyst/merge_registry.py
- [registry-queue-watchers](registry-queue-watchers.md) — registry & queue watchers · scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [secret-hygiene](secret-hygiene.md) — secret hygiene · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, scripts/session-brief.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [sentry-client](sentry-client.md) — Sentry Client · dashboard/sentry_client.py
- [sentry-heartbeat](sentry-heartbeat.md) — Sentry heartbeat · scripts/core/sentry-heartbeat.sh
- [session-context-tooling](session-context-tooling.md) — session & context tooling · scripts/core/directive_writer.py, scripts/ops/context7-check.py, scripts/session-brief.py, tests/test_context7_check.sh, tests/test_directive_section_refs.sh
- [set-e-shape-lint](set-e-shape-lint.md) — set -e shape lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-waitlist](snapog-landing-waitlist.md) — SnapOG Landing & Waitlist · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-schema](snapog-schema.md) — SnapOG Schema · docs/operations/north-star-metric-query.sql, projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-smoke-tests](snapog-smoke-tests.md) — SnapOG Smoke Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/types.ts
- [telegram-notification-channel](telegram-notification-channel.md) — Telegram notification channel · scripts/core/telegram-notify.sh, scripts/ops/bloat-trend.py, scripts/ops/directive-staleness-watch.py, scripts/ops/docker-prune-safe.sh, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [test-by-extraction-strategy](test-by-extraction-strategy.md) — test-by-extraction strategy · tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_cycle_metadata.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_seteshape_lint.py
- [threshold-pinning-against-drift](threshold-pinning-against-drift.md) — threshold pinning against drift · scripts/ops/turn-audit.py, tests/test_turn_audit.sh
- [tool-usage-audit-engine](tool-usage-audit-engine.md) — tool-usage audit engine · scripts/ops/tool-usage-audit.py
- [tool-usage-audit-regression-suite](tool-usage-audit-regression-suite.md) — tool-usage audit regression suite · tests/test_tool_usage_audit.sh
- [turn-audit-policy-engine](turn-audit-policy-engine.md) — turn-audit policy engine · scripts/ops/turn-audit.py
- [turn-audit-regression-suite](turn-audit-regression-suite.md) — turn-audit regression suite · tests/test_turn_audit.sh
- [turn-economy-trend-watcher](turn-economy-trend-watcher.md) — turn-economy trend watcher · scripts/ops/bloat-trend.py
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

62 per-file wiring cards mirror the source tree under `graft/` (60 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
