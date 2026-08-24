# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-access-layer](airtable-access-layer.md) — Airtable access layer · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [airtable-read-write-guards](airtable-read-write-guards.md) — Airtable read/write guards · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, tests/test_airtable_read.sh, tests/test_airtable_write.sh
- [atomic-state-writes](atomic-state-writes.md) — Atomic state writes · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py
- [auto-loop-core-engine](auto-loop-core-engine.md) — Auto-loop core engine · scripts/core/auto-loop.sh
- [budget-and-spend-accounting](budget-and-spend-accounting.md) — Budget and spend accounting · scripts/core/auto-loop.sh, scripts/core/engine-usage-cost.py, tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_codex_spend_sources.sh, tests/test_cost_model_hint.sh, tests/test_tier_ladder_daily.sh
- [compliance-directive-audits](compliance-directive-audits.md) — Compliance & directive audits · scripts/ops/context7-check.py, scripts/ops/directive-rule-sweep.py, scripts/ops/directive-staleness-watch.py
- [context7-and-browse-extract-ops](context7-and-browse-extract-ops.md) — Context7 and browse-extract ops · scripts/ops/browse-extract.py, scripts/ops/context7-check.py, tests/test_browse_extract.sh, tests/test_context7_check.sh
- [cost-budget-reporting](cost-budget-reporting.md) — Cost & budget reporting · scripts/ops/bloat-trend.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py, scripts/ops/state-snapshot.py
- [cycle-metadata-and-engine-routing](cycle-metadata-and-engine-routing.md) — Cycle metadata and engine routing · scripts/core/auto-loop.sh, tests/test_cycle_metadata.sh, tests/test_mixed_harness.sh
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/server.py, tests/test_dashboard_server.py
- [docker-host-hygiene](docker-host-hygiene.md) — Docker & host hygiene · scripts/ops/docker-prune-safe.sh, scripts/ops/opportunity-analyst-cron.sh
- [engine-cost-pricing](engine-cost-pricing.md) — Engine cost pricing · scripts/core/engine-usage-cost.py, tests/test_cost_model_hint.sh
- [escalation-and-operator-requests](escalation-and-operator-requests.md) — Escalation and operator requests · scripts/core/auto-loop.sh, scripts/core/operator_request_notify.py, tests/test_escalation.sh, tests/test_operator_request_notify.py, tests/test_refusal_format.sh
- [fail-closed-determinism](fail-closed-determinism.md) — Fail-closed determinism · scripts/core/jcode-mcp-probe.py, scripts/ops/airtable-write.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [fail-open-vs-fail-closed-policy](fail-open-vs-fail-closed-policy.md) — Fail-open vs fail-closed policy · scripts/core/auto-loop.sh, scripts/core/jcode-mcp-config.py, scripts/ops/send-gate.py, scripts/prod-mechanism-guard.py, tests/test_ccusage_failclosed.sh, tests/test_idle_skip.sh, tests/test_jcode_mcp_config.sh, tests/test_send_gate.sh
- [g4-identity-matching](g4-identity-matching.md) — G4 identity matching · scripts/ops/g4-check.py, tests/test_g4_check.sh
- [idle-skip-and-discretionary-budget](idle-skip-and-discretionary-budget.md) — Idle-skip and discretionary budget · scripts/core/auto-loop.sh, scripts/ops/idle-skip-note.py, tests/test_discretionary_budget.sh, tests/test_idle_skip.sh
- [idle-skip-audit-trail](idle-skip-audit-trail.md) — Idle-skip audit trail · scripts/ops/idle-skip-note.py
- [jcode-event-stream-utilities](jcode-event-stream-utilities.md) — jcode event-stream utilities · scripts/core/jcode-final-text.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [linear-workstream-discipline](linear-workstream-discipline.md) — Linear workstream discipline · scripts/ops/linear-track.py
- [loop-lifecycle-monitoring-shell](loop-lifecycle-monitoring-shell.md) — Loop lifecycle & monitoring (shell) · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [mcp-boot-config-generation](mcp-boot-config-generation.md) — MCP boot & config generation · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py
- [mcp-configuration-and-probe](mcp-configuration-and-probe.md) — MCP configuration and probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, tests/fixtures/mock_mcp_server.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_probe.sh
- [mcp-key-fallback](mcp-key-fallback.md) — MCP key fallback · tests/test_mcp_key_fallback.sh
- [operator-escalation-notification](operator-escalation-notification.md) — Operator escalation & notification · scripts/core/operator_request_notify.py, scripts/core/telegram-notify.sh, scripts/ops/directive-staleness-watch.py, scripts/ops/operator-usage-report.sh, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [outreach-eligibility-gate](outreach-eligibility-gate.md) — Outreach eligibility gate · scripts/ops/g4-check.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [prod-mechanism-guard](prod-mechanism-guard.md) — Prod-mechanism guard · scripts/prod-mechanism-guard.py, tests/test_prod_mechanism_guard.sh
- [prompt-assembly-and-transport](prompt-assembly-and-transport.md) — Prompt assembly and transport · scripts/core/auto-loop.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh
- [registry-evidence-extraction](registry-evidence-extraction.md) — Registry & evidence extraction · scripts/ops/context7-check.py, scripts/ops/extract-axis-evidence.py, scripts/ops/kik-decision-read.py, scripts/ops/registry-archive.py
- [registry-operations](registry-operations.md) — Registry operations · scripts/ops/registry-archive.py, scripts/ops/registry-queue-watch.py, tests/test_registry_archive.sh, tests/test_registry_queue_watch.sh
- [secret-handling](secret-handling.md) — Secret handling · scripts/core/jcode-mcp-config.py, scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh, scripts/ops/linear-track.py, scripts/ops/verify-mcp-keys.py
- [secret-hygiene](secret-hygiene.md) — Secret hygiene · scripts/core/jcode-mcp-config.py, scripts/session-brief.py, tests/test_jcode_mcp_config.sh, tests/test_mcp_key_fallback.sh
- [send-gate-and-outreach-policy](send-gate-and-outreach-policy.md) — Send gate and outreach policy · scripts/ops/reply-watch.py, scripts/ops/send-gate.py, tests/test_reply_watch.sh, tests/test_send_gate.sh
- [session-and-wsl-daemon-tooling](session-and-wsl-daemon-tooling.md) — Session and WSL daemon tooling · scripts/session-brief.py, scripts/wsl/install-wsl-daemon.sh, scripts/wsl/uninstall-wsl-daemon.sh, scripts/wsl/wsl-daemon-status.sh
- [set-e-lint](set-e-lint.md) — Set-e lint · docker-entrypoint.sh, scripts/core/auto-loop.sh, tests/test_seteshape_lint.py
- [test-by-extraction-strategy](test-by-extraction-strategy.md) — Test-by-extraction strategy · tests/test_budget_gates.sh, tests/test_ccusage_failclosed.sh, tests/test_cycle_metadata.sh, tests/test_escalation.sh, tests/test_idle_skip.sh, tests/test_mixed_harness.sh, tests/test_prompt_assembly.sh, tests/test_prompt_transport.sh, tests/test_tier_ladder_daily.sh
- [tool-usage-audit](tool-usage-audit.md) — Tool usage audit · scripts/ops/tool-usage-audit.py, tests/test_tool_usage_audit.sh
- [turn-audit-policy-script](turn-audit-policy-script.md) — turn-audit policy script · scripts/ops/turn-audit.py
- [turn-audit-regression-suite](turn-audit-regression-suite.md) — turn-audit regression suite · tests/test_turn_audit.sh
- [web-research-cost-model](web-research-cost-model.md) — Web research cost model · scripts/ops/web-research-cost.py

## Files

61 per-file wiring cards mirror the source tree under `graft/` (59 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
