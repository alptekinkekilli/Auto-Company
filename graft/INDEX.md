# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-read](airtable-read.md) — airtable-read · scripts/ops/airtable-read.py
- [airtable-read-write-guards](airtable-read-write-guards.md) — Airtable read/write guards · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [airtable-write](airtable-write.md) — airtable-write · scripts/ops/airtable-write.py
- [analyst-engine](analyst-engine.md) — Analyst engine · scripts/analyst/opportunity-analyst-jcode.sh
- [anchor-string-consistency](anchor-string-consistency.md) — Anchor string consistency · tests/test_compact_anchor_sync.py, tests/test_compact_ritual_hardening.sh
- [atomic-write-discipline](atomic-write-discipline.md) — atomic-write-discipline · scripts/core/directive_writer.py, scripts/core/jcode-mcp-config.py, scripts/core/operator_request_notify.py, scripts/ops/cost-audit.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py
- [audit-tools-turn-tool-state](audit-tools-turn-tool-state.md) — audit tools (turn/tool/state) · scripts/ops/state-snapshot.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [auto-company-site-functions](auto-company-site-functions.md) — Auto-Company Site Functions · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [auto-loop](auto-loop.md) — Auto Loop · scripts/core/auto-loop.sh
- [auto-loop-core-engine](auto-loop-core-engine.md) — auto-loop core engine · scripts/core/auto-loop.sh
- [auto-loop-sh-core-loop](auto-loop-sh-core-loop.md) — auto-loop.sh core loop · scripts/core/auto-loop.sh
- [bloat-trend](bloat-trend.md) — bloat-trend · scripts/ops/bloat-trend.py
- [bridge-leak-scanner](bridge-leak-scanner.md) — Bridge Leak Scanner · scripts/core/bridge_leak_scan.py
- [browse-extract](browse-extract.md) — browse-extract · scripts/ops/browse-extract.py
- [browse-extract-mcp-client](browse-extract-mcp-client.md) — Browse extract MCP client · scripts/ops/browse-extract.py
- [budget-calibration-report](budget-calibration-report.md) — budget-calibration-report · scripts/ops/budget-calibration-report.py
- [cli-final-text-extractors](cli-final-text-extractors.md) — CLI Final-Text Extractors · scripts/core/codex-final-text.py
- [cockpit-dashboard](cockpit-dashboard.md) — Cockpit Dashboard · dashboard/app.js, dashboard/sentry_client.py, dashboard/server.py
- [codex-spend-accounting](codex-spend-accounting.md) — Codex spend accounting · scripts/core/codex-final-text.py
- [compact-ritual](compact-ritual.md) — Compact ritual · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-resume-lint.py
- [compact-ritual-hooks](compact-ritual-hooks.md) — Compact Ritual Hooks · scripts/compact-postcheck.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/compact-resume-lint.py, scripts/context-watch.py
- [container-entrypoint](container-entrypoint.md) — Container Entrypoint · docker-entrypoint.sh
- [content-hash-provenance](content-hash-provenance.md) — content-hash-provenance · scripts/core/decision_text_hash.py, scripts/ops/kik-decision-read.py
- [context7-check](context7-check.md) — context7-check · scripts/ops/context7-check.py
- [cost-audit](cost-audit.md) — cost-audit · scripts/ops/cost-audit.py
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py
- [decision-text-hash](decision-text-hash.md) — decision_text_hash · scripts/core/decision_text_hash.py
- [deterministic-gates-over-llm-trust](deterministic-gates-over-llm-trust.md) — Deterministic Gates over LLM Trust · scripts/analyst/merge_registry.py, scripts/analyst/promote_directive.py, scripts/core/bridge_leak_scan.py
- [directive-rule-sweep](directive-rule-sweep.md) — directive-rule-sweep · scripts/ops/directive-rule-sweep.py
- [directive-staleness-watch](directive-staleness-watch.md) — directive-staleness-watch · scripts/ops/directive-staleness-watch.py
- [directive-writer](directive-writer.md) — Directive Writer · scripts/core/directive_writer.py
- [docker-prune-safe](docker-prune-safe.md) — docker-prune-safe · scripts/ops/docker-prune-safe.sh
- [engine-usage-cost](engine-usage-cost.md) — engine-usage-cost · scripts/core/engine-usage-cost.py
- [extract-axis-evidence](extract-axis-evidence.md) — extract-axis-evidence · scripts/ops/extract-axis-evidence.py
- [extract-real-code-test-strategy](extract-real-code-test-strategy.md) — Extract-real-code test strategy · tests/test_active_window.sh, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cycle_counter.sh, tests/test_cycle_metadata.sh, tests/test_discretionary_budget.sh, tests/test_escalation.sh, tests/test_idle_skip.sh
- [fail-closed-evidence](fail-closed-evidence.md) — fail-closed-evidence · scripts/core/directive_writer.py, scripts/core/jcode-mcp-probe.py, scripts/ops/airtable-write.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py
- [fail-closed-measurement-invariant](fail-closed-measurement-invariant.md) — Fail-closed measurement invariant · scripts/core/auto-loop.sh, scripts/ops/rfq-send.py, scripts/ops/send-gate.py, scripts/ops/verify-mcp-keys.py, scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [fail-open-monitoring](fail-open-monitoring.md) — Fail-Open Monitoring · dashboard/sentry_client.py, projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/webhook.ts, scripts/analyst/merge_registry.py, scripts/analyst/promote_directive.py, scripts/compact-preflight.py, scripts/compact-report.py, scripts/core/bridge_leak_scan.py
- [g4-attribution-evidence](g4-attribution-evidence.md) — G4 attribution evidence · scripts/ops/g4-check.py, scripts/ops/site-contact-evidence.py
- [g4-attribution-matching](g4-attribution-matching.md) — G4 attribution matching · scripts/ops/g4-check.py, scripts/ops/site-contact-evidence.py, tests/test_g4_check.sh
- [g4-check](g4-check.md) — g4-check · scripts/ops/g4-check.py
- [graft-auto-refresh](graft-auto-refresh.md) — graft-auto-refresh · scripts/graft-auto-refresh.py
- [headinspect-grading](headinspect-grading.md) — HeadInspect Grading · projects/headinspect/src/inspect.ts
- [headinspect-worker](headinspect-worker.md) — HeadInspect Worker · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [idle-skip-discretionary-budget](idle-skip-discretionary-budget.md) — Idle skip & discretionary budget · scripts/ops/idle-skip-note.py
- [idle-skip-note](idle-skip-note.md) — idle-skip-note · scripts/ops/idle-skip-note.py
- [jcode-final-text](jcode-final-text.md) — jcode-final-text · scripts/core/jcode-final-text.py
- [jcode-mcp-config](jcode-mcp-config.md) — jcode-mcp-config · scripts/core/jcode-mcp-config.py
- [jcode-mcp-probe](jcode-mcp-probe.md) — jcode-mcp-probe · scripts/core/jcode-mcp-probe.py
- [jcode-pilot-smoke-test](jcode-pilot-smoke-test.md) — jcode Pilot Smoke Test · scripts/analyst/jcode-pilot-smoke.sh
- [kik-decision-read](kik-decision-read.md) — kik-decision-read · scripts/ops/kik-decision-read.py
- [linear-track](linear-track.md) — linear-track · scripts/ops/linear-track.py
- [linux-runtime-scripts](linux-runtime-scripts.md) — linux-runtime-scripts · scripts/linux/noop-action.sh, scripts/linux/status-linux.sh
- [macos-runtime-scripts](macos-runtime-scripts.md) — macos-runtime-scripts · scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [mcp-config-generation](mcp-config-generation.md) — MCP config generation · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py
- [mcp-config-sync-invariant](mcp-config-sync-invariant.md) — MCP config sync invariant · tests/test_jcode_mcp_config.sh, tests/test_mcp_config_manifest_sync.sh, tests/test_mcp_key_fallback.sh, tests/test_mcp_probe.sh
- [mcp-key-verification](mcp-key-verification.md) — MCP key verification · scripts/ops/verify-mcp-keys.py
- [mcp-mock-server-fixture](mcp-mock-server-fixture.md) — MCP mock server fixture · tests/fixtures/mock_mcp_server.py
- [mixed-harness-metadata-attribution](mixed-harness-metadata-attribution.md) — mixed harness metadata attribution · scripts/core/auto-loop.sh, tests/test_mixed_harness.sh
- [monitor](monitor.md) — monitor · scripts/core/monitor.sh
- [operator-action-router](operator-action-router.md) — operator-action-router · scripts/ops/operator-action-router.py
- [operator-action-router-py](operator-action-router-py.md) — operator-action-router.py · scripts/ops/operator-action-router.py
- [operator-escalation](operator-escalation.md) — operator-escalation · scripts/core/operator_request_notify.py, scripts/ops/directive-staleness-watch.py, scripts/ops/operator-action-router.py, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [operator-request-ledger](operator-request-ledger.md) — Operator Request Ledger · dashboard/server.py
- [operator-request-notify](operator-request-notify.md) — operator_request_notify · scripts/core/operator_request_notify.py
- [operator-request-notify-py](operator-request-notify-py.md) — operator_request_notify.py · scripts/core/operator_request_notify.py
- [operator-usage-report](operator-usage-report.md) — operator-usage-report · scripts/ops/operator-usage-report.sh
- [opportunity-analyst](opportunity-analyst.md) — Opportunity Analyst · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh, scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — opportunity-analyst-cron · scripts/ops/opportunity-analyst-cron.sh
- [outcome-watchers-reply-rfq](outcome-watchers-reply-rfq.md) — outcome watchers (reply/rfq) · scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py, scripts/ops/rfq-reply-watch.py
- [outreach-eligibility-gate](outreach-eligibility-gate.md) — Outreach eligibility gate · scripts/ops/send-gate.py
- [prod-mechanism-guard-py](prod-mechanism-guard-py.md) — prod-mechanism-guard.py · scripts/prod-mechanism-guard.py
- [prod-mechanism-guard-tripwire](prod-mechanism-guard-tripwire.md) — Prod-mechanism guard tripwire · scripts/prod-mechanism-guard.py
- [promotion-gate](promotion-gate.md) — Promotion Gate · scripts/analyst/promote_directive.py
- [prompt-assembly-contract](prompt-assembly-contract.md) — prompt assembly contract · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh
- [prompt-transport-contract](prompt-transport-contract.md) — prompt transport contract · scripts/core/auto-loop.sh, tests/test_prompt_transport.sh
- [refusal-format-contract](refusal-format-contract.md) — refusal format contract · dashboard/server.py, scripts/core/operator_request_notify.py, tests/test_refusal_format.sh
- [registry-archive](registry-archive.md) — registry-archive · scripts/ops/registry-archive.py
- [registry-archive-py](registry-archive-py.md) — registry-archive.py · scripts/ops/registry-archive.py
- [registry-queue-watch](registry-queue-watch.md) — registry-queue-watch · scripts/ops/registry-queue-watch.py
- [reply-watch](reply-watch.md) — reply-watch · scripts/ops/reply-watch.py
- [rfq-reply-watcher-advisory](rfq-reply-watcher-advisory.md) — RFQ reply watcher (advisory) · scripts/ops/rfq-reply-watch.py
- [rfq-send-py](rfq-send-py.md) — rfq-send.py · scripts/ops/rfq-send.py
- [rfq-send-tool](rfq-send-tool.md) — RFQ send tool · scripts/ops/rfq-send.py
- [rfq-template](rfq-template.md) — rfq-template · scripts/ops/rfq_template.py
- [secret-handling](secret-handling.md) — secret-handling · scripts/core/jcode-mcp-config.py, scripts/core/telegram-notify.sh, scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh
- [secret-hygiene-no-argv-leaks](secret-hygiene-no-argv-leaks.md) — Secret hygiene (no argv leaks) · scripts/core/jcode-mcp-config.py, scripts/ops/verify-mcp-keys.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [send-gate-py](send-gate-py.md) — send-gate.py · scripts/ops/send-gate.py
- [sentry-heartbeat](sentry-heartbeat.md) — sentry-heartbeat · scripts/core/sentry-heartbeat.sh
- [sentry-reporter](sentry-reporter.md) — Sentry Reporter · dashboard/sentry_client.py
- [session-brief-hook](session-brief-hook.md) — Session brief hook · scripts/session-brief.py
- [set-e-shape-lint](set-e-shape-lint.md) — set -e shape lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [site-contact-evidence](site-contact-evidence.md) — site-contact-evidence · scripts/ops/site-contact-evidence.py
- [snapog-cost-alerts](snapog-cost-alerts.md) — SnapOG Cost Alerts · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-landing](snapog-landing.md) — SnapOG Landing · projects/_archive/snapog/src/dashboard/pages.ts
- [snapog-worker](snapog-worker.md) — SnapOG Worker · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [state-snapshot-probe](state-snapshot-probe.md) — State snapshot probe · scripts/ops/state-snapshot.py
- [stop-loop](stop-loop.md) — stop-loop · scripts/core/stop-loop.sh
- [telegram-notify](telegram-notify.md) — telegram-notify · scripts/core/telegram-notify.sh
- [tier-ladder-budget-selection](tier-ladder-budget-selection.md) — tier ladder budget selection · scripts/core/auto-loop.sh, tests/test_tier_ladder_daily.sh
- [tool-usage-analytics](tool-usage-analytics.md) — Tool usage analytics · scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py, scripts/ops/web-research-cost.py
- [wowcar-revenue-relabel-acceptance](wowcar-revenue-relabel-acceptance.md) — Wowcar revenue relabel acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py
- [wowcar-revenue-vocabulary-acceptance](wowcar-revenue-vocabulary-acceptance.md) — wowcar revenue vocabulary acceptance · scripts/ops/wowcar-revenue-vocabulary-acceptance.py, tests/test_wowcar_revenue_vocabulary_acceptance.sh
- [wsl-daemon-lifecycle](wsl-daemon-lifecycle.md) — WSL daemon lifecycle · scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh

## Files

82 per-file wiring cards mirror the source tree under `graft/` (80 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
