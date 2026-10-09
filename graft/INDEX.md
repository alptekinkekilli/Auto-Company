# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-wrappers](airtable-access-wrappers.md) — Airtable Access Wrappers · tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [airtable-read-write-wrappers](airtable-read-write-wrappers.md) — Airtable read/write wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [analyst-engine](analyst-engine.md) — Analyst Engine · tests/test_analyst_engine.sh
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop-harness](auto-loop-harness.md) — Auto-Loop Harness · tests/test_active_window.sh, tests/test_auto_loop_consensus_prune.sh, tests/test_auto_loop_ledger_guard.sh, tests/test_auto_loop_work_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh
- [autonomous-loop-orchestrator](autonomous-loop-orchestrator.md) — Autonomous Loop Orchestrator · scripts/core/auto-loop.sh
- [browse-and-extract-harness](browse-and-extract-harness.md) — Browse-and-extract harness · scripts/ops/browse-extract.py
- [browse-extraction](browse-extraction.md) — Browse Extraction · tests/test_browse_extract.sh
- [budget-calibration-cost-audit](budget-calibration-cost-audit.md) — Budget calibration & cost audit · scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [compact-ritual-hardening](compact-ritual-hardening.md) — Compact Ritual Hardening · tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh
- [compact-ritual-path-resolution](compact-ritual-path-resolution.md) — Compact Ritual Path Resolution · scripts/compact_yol.py, tests/test_compact_yol.py
- [compact-ritual-tooling](compact-ritual-tooling.md) — Compact Ritual Tooling · scripts/compact_yol.py, scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py
- [consensus-pruning](consensus-pruning.md) — Consensus Pruning · tests/test_auto_loop_consensus_prune.sh, tests/test_consensus_prune.py
- [consensus-registry-maintenance](consensus-registry-maintenance.md) — Consensus & registry maintenance · scripts/ops/consensus-prune.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [container-bootstrap](container-bootstrap.md) — Container Bootstrap · docker-entrypoint.sh
- [content-hash-provenance-decision-text-hash](content-hash-provenance-decision-text-hash.md) — Content-hash provenance (decision_text_hash) · scripts/core/decision_text_hash.py, scripts/ops/kik-decision-read.py
- [context-watch-hook](context-watch-hook.md) — Context Watch Hook · scripts/context-watch.py
- [context7-compliance-checker](context7-compliance-checker.md) — Context7 compliance checker · scripts/ops/context7-check.py
- [context7-docs-wrapper](context7-docs-wrapper.md) — Context7 Docs Wrapper · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
- [context7-import-audit](context7-import-audit.md) — Context7 Import Audit · tests/test_context7_check.sh
- [cycle-economics-cost-auditing](cycle-economics-cost-auditing.md) — Cycle Economics & Cost Auditing · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py, tests/test_cost_audit_tool_surface.py, tests/test_cost_model_hint.sh
- [directive-staleness-rule-sweep](directive-staleness-rule-sweep.md) — Directive staleness & rule sweep · scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [directive-write-gate](directive-write-gate.md) — Directive Write Gate · dashboard/server.py, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [docker-disk-space-guard](docker-disk-space-guard.md) — Docker disk-space guard · scripts/ops/docker-prune-safe.sh
- [engine-usage-cost-adapter](engine-usage-cost-adapter.md) — Engine usage cost adapter · scripts/core/engine-usage-cost.py
- [evidence-extraction-axis-screening](evidence-extraction-axis-screening.md) — Evidence extraction & axis screening · scripts/ops/extract-axis-evidence.py
- [final-text-extraction-codex-jcode](final-text-extraction-codex-jcode.md) — Final-text extraction (codex/jcode) · scripts/core/codex-final-text.py, scripts/core/jcode-final-text.py
- [g4-attribution-evidence](g4-attribution-evidence.md) — G4 Attribution Evidence · scripts/ops/site-contact-evidence.py
- [g4-identity-attribution-checker](g4-identity-attribution-checker.md) — G4 identity-attribution checker · scripts/ops/g4-check.py
- [graft-auto-refresh](graft-auto-refresh.md) — Graft auto-refresh · scripts/graft-auto-refresh.py
- [headinspect-service](headinspect-service.md) — HeadInspect Service · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [human-directive-writer-directive-writer](human-directive-writer-directive-writer.md) — Human directive writer (directive_writer) · scripts/core/directive_writer.py
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-decision-reader](ki-k-decision-reader.md) — KİK decision reader · scripts/ops/kik-decision-read.py
- [ledger-integrity-guard](ledger-integrity-guard.md) — Ledger integrity guard · scripts/ops/ledger-guard.py
- [linear-workstream-tracker](linear-workstream-tracker.md) — Linear workstream tracker · scripts/ops/linear-track.py
- [loop-lifecycle-monitoring-shell](loop-lifecycle-monitoring-shell.md) — Loop lifecycle & monitoring (shell) · scripts/core/monitor.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [mcp-config-generation-boot-probe](mcp-config-generation-boot-probe.md) — MCP config generation & boot probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-key-verification](mcp-key-verification.md) — MCP Key Verification · scripts/ops/verify-mcp-keys.py
- [mcp-probe-test-fixture](mcp-probe-test-fixture.md) — MCP Probe Test Fixture · tests/fixtures/mock_mcp_server.py
- [operator-alerting-watchers](operator-alerting-watchers.md) — Operator Alerting Watchers · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py
- [operator-escalation-notification](operator-escalation-notification.md) — Operator escalation & notification · scripts/core/operator_request_notify.py, scripts/core/telegram-notify.sh, scripts/ops/operator-action-router.py
- [operator-usage-reporter](operator-usage-reporter.md) — Operator usage reporter · scripts/ops/operator-usage-report.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — Opportunity Analyst cron · scripts/ops/opportunity-analyst-cron.sh
- [outreach-eligibility-gate-send-gate](outreach-eligibility-gate-send-gate.md) — Outreach Eligibility Gate (send-gate) · scripts/ops/send-gate.py
- [production-mechanism-guard](production-mechanism-guard.md) — Production Mechanism Guard · scripts/prod-mechanism-guard.py, tests/test_auto_loop_consensus_prune.sh
- [registry-merge-tool](registry-merge-tool.md) — Registry Merge Tool · scripts/analyst/merge_registry.py
- [rfq-email-sending-templating](rfq-email-sending-templating.md) — RFQ Email Sending & Templating · scripts/ops/rfq_template.py, scripts/ops/rfq-send.py
- [sentry-heartbeat](sentry-heartbeat.md) — Sentry heartbeat · scripts/core/sentry-heartbeat.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-hook](session-brief-hook.md) — Session Brief Hook · scripts/session-brief.py, tests/test_compact_ritual_hardening.sh
- [session-leak-scanner-bridge-leak-scan](session-leak-scanner-bridge-leak-scan.md) — Session-leak scanner (bridge_leak_scan) · scripts/core/bridge_leak_scan.py
- [site-contact-evidence-examiner](site-contact-evidence-examiner.md) — Site contact evidence examiner · scripts/ops/g4-check.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing-dashboard](snapog-landing-dashboard.md) — SnapOG Landing/Dashboard · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-north-star-metric](snapog-north-star-metric.md) — SnapOG North-Star Metric · docs/operations/north-star-metric-query.sql
- [snapog-service](snapog-service.md) — SnapOG Service · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-validation-scripts](snapog-validation-scripts.md) — SnapOG Validation Scripts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [state-snapshot-probe](state-snapshot-probe.md) — State Snapshot Probe · scripts/ops/state-snapshot.py
- [turn-bloat-escalation](turn-bloat-escalation.md) — Turn Bloat Escalation · scripts/ops/turn-bloat-brake.py, tests/test_auto_loop_ledger_guard.sh
- [turn-economy-trend-bloat-watcher](turn-economy-trend-bloat-watcher.md) — Turn-economy trend & bloat watcher · scripts/ops/bloat-trend.py
- [work-window-brake-watchdog](work-window-brake-watchdog.md) — Work-Window Brake & Watchdog · scripts/ops/work-window-watchdog.py, scripts/ops/work-window.py, tests/test_auto_loop_work_window.sh
- [wowcar-revenue-vocabulary-acceptance](wowcar-revenue-vocabulary-acceptance.md) — Wowcar Revenue Vocabulary Acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wsl-daemon-management](wsl-daemon-management.md) — WSL Daemon Management · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

86 per-file wiring cards mirror the source tree under `graft/` (84 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
