# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-layer](airtable-access-layer.md) — Airtable access layer · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [airtable-ops-wrappers](airtable-ops-wrappers.md) — Airtable ops wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [atomic-write-read-back-verification](atomic-write-read-back-verification.md) — Atomic write & read-back verification · scripts/core/jcode-mcp-config.py, scripts/core/operator_request_notify.py, scripts/ops/airtable-write.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-core-engine](auto-loop-core-engine.md) — Auto-loop core engine · scripts/core/auto-loop.sh
- [autonomous-loop](autonomous-loop.md) — Autonomous Loop · scripts/core/auto-loop.sh
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [browse-extract-harness](browse-extract-harness.md) — browse-extract harness · scripts/ops/browse-extract.py
- [budget-spend-accounting](budget-spend-accounting.md) — Budget & spend accounting · scripts/core/auto-loop.sh, scripts/core/engine-usage-cost.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cost_model_hint.sh, tests/test_tier_ladder_daily.sh
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — Content-Hash Provenance · scripts/core/decision_text_hash.py
- [context-directive-integrity](context-directive-integrity.md) — Context & directive integrity · scripts/core/directive_writer.py, scripts/ops/context7-check.py, tests/test_context7_check.sh, tests/test_directive_section_refs.sh
- [context-watch-compact-preflight](context-watch-compact-preflight.md) — Context Watch & Compact Preflight · scripts/compact-preflight.py, scripts/context-watch.py
- [cost-accounting](cost-accounting.md) — Cost Accounting · scripts/core/engine-usage-cost.py
- [cost-budget-calibration](cost-budget-calibration.md) — Cost & budget calibration · scripts/ops/bloat-trend.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py, scripts/ops/operator-usage-report.sh
- [dashboard-runtime-telemetry](dashboard-runtime-telemetry.md) — Dashboard & runtime telemetry · dashboard/server.py, tests/test_dashboard_server.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [docker-host-disk-guard](docker-host-disk-guard.md) — Docker & host disk guard · scripts/ops/docker-prune-safe.sh
- [fail-closed-verification-invariant](fail-closed-verification-invariant.md) — Fail-closed verification invariant · scripts/core/jcode-mcp-probe.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [g4-verification-entity-matching](g4-verification-entity-matching.md) — G4 verification & entity matching · scripts/ops/g4-check.py, tests/test_g4_check.sh
- [headinspect-privacy-invariant](headinspect-privacy-invariant.md) — HeadInspect Privacy Invariant · projects/headinspect/migrations/0001_hits.sql
- [headinspect-service](headinspect-service.md) — HeadInspect Service · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [jcode-event-stream-utilities](jcode-event-stream-utilities.md) — jcode event-stream utilities · scripts/core/jcode-final-text.py, scripts/ops/context7-check.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [jcode-mcp-config-probe](jcode-mcp-config-probe.md) — jcode MCP config & probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-linear-workstream-tooling](ki-k-linear-workstream-tooling.md) — KİK & Linear workstream tooling · scripts/ops/kik-decision-read.py, scripts/ops/linear-track.py
- [loop-lifecycle-monitoring](loop-lifecycle-monitoring.md) — Loop lifecycle & monitoring · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [mcp-config-key-handling](mcp-config-key-handling.md) — MCP config & key handling · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [operator-escalation](operator-escalation.md) — Operator escalation · scripts/core/auto-loop.sh, tests/test_escalation.sh
- [operator-escalation-notification](operator-escalation-notification.md) — Operator escalation & notification · scripts/core/operator_request_notify.py, scripts/core/telegram-notify.sh, scripts/ops/directive-staleness-watch.py, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [operator-request-lifecycle](operator-request-lifecycle.md) — Operator request lifecycle · scripts/core/operator_request_notify.py, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — Opportunity Analyst cron · scripts/ops/opportunity-analyst-cron.sh
- [outreach-eligibility-g4-verification](outreach-eligibility-g4-verification.md) — Outreach eligibility & G4 verification · scripts/ops/g4-check.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [outreach-send-gating](outreach-send-gating.md) — Outreach & send gating · scripts/ops/reply-watch.py, scripts/ops/send-gate.py, tests/test_reply_watch.sh, tests/test_send_gate.sh
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [prompt-assembly-guardrails](prompt-assembly-guardrails.md) — Prompt assembly guardrails · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh
- [prompt-transport-contract](prompt-transport-contract.md) — Prompt transport contract · scripts/core/auto-loop.sh, tests/test_prompt_transport.sh
- [registry-directive-hygiene](registry-directive-hygiene.md) — Registry & directive hygiene · scripts/ops/directive-rule-sweep.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py
- [registry-merge-invariants](registry-merge-invariants.md) — Registry Merge Invariants · scripts/analyst/merge_registry.py
- [registry-pipeline](registry-pipeline.md) — Registry pipeline · scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [secret-handling-discipline](secret-handling-discipline.md) — Secret handling discipline · scripts/core/jcode-mcp-config.py, scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh, scripts/ops/linear-track.py, scripts/ops/verify-mcp-keys.py
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-context-injection](session-context-injection.md) — Session & context injection · scripts/session-brief.py
- [set-e-shape-lint](set-e-shape-lint.md) — Set-e shape lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-sample-tests](snapog-sample-tests.md) — SnapOG Sample Tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/dashboard/pages.ts, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot-idle-detection](state-snapshot-idle-detection.md) — State snapshot & idle detection · scripts/ops/idle-skip-note.py, scripts/ops/state-snapshot.py, tests/test_idle_skip.sh, tests/test_state_snapshot.sh
- [state-snapshot-idle-skip-audit-trail](state-snapshot-idle-skip-audit-trail.md) — State snapshot & idle-skip audit trail · scripts/ops/idle-skip-note.py, scripts/ops/state-snapshot.py
- [tool-usage-audit](tool-usage-audit.md) — Tool usage audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-audit-policy-script](turn-audit-policy-script.md) — turn-audit policy script · scripts/ops/turn-audit.py
- [turn-audit-regression-suite](turn-audit-regression-suite.md) — turn-audit regression suite · tests/test_turn_audit.sh
- [web-research-cost-model](web-research-cost-model.md) — Web research cost model · scripts/ops/web-research-cost.py
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

61 per-file wiring cards mirror the source tree under `graft/` (59 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
