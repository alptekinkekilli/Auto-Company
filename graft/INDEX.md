# graft — repo map

Small markdown nodes summarising this repo. `grep` any term, symbol, or
filename here, or run `graft ask "<task>"`. Each node carries prose plus exact
`file:line`; open a source file only to edit the named span.

The same graph is queryable as MCP tools (`graft_find_code`, `graft_find_all`,
`graft_trace_calls`, `graft_file_api`, `graft_repo_map`) where a host exposes them, and
as the `graft` CLI everywhere else. Edges — who calls what — live only in the
graph, not in these files: `graft callers <symbol>` is the only way to read them.

## Concepts

- [airtable-ops-wrappers](airtable-ops-wrappers.md) — Airtable ops wrappers · scripts/ops/airtable-read.py, scripts/ops/airtable-write.py
- [atomic-write-read-back-verification](atomic-write-read-back-verification.md) — Atomic write & read-back verification · scripts/core/jcode-mcp-config.py, scripts/core/operator_request_notify.py, scripts/ops/airtable-write.py, scripts/ops/idle-skip-note.py, scripts/ops/registry-archive.py, scripts/ops/state-snapshot.py
- [auto-company-autonomous-loop-core](auto-company-autonomous-loop-core.md) — Auto Company autonomous loop core · scripts/core/auto-loop.sh
- [auto-company-site-branded-endpoints](auto-company-site-branded-endpoints.md) — Auto-company site branded endpoints · projects/auto-company-site/functions/listeden-cik.js, projects/auto-company-site/functions/randevu.js
- [browse-extract-harness](browse-extract-harness.md) — browse-extract harness · scripts/ops/browse-extract.py
- [canonical-content-hashing-for-ki-k-decisions](canonical-content-hashing-for-ki-k-decisions.md) — Canonical content hashing for KİK decisions · scripts/core/decision_text_hash.py
- [container-bootstrap-and-state-persistence](container-bootstrap-and-state-persistence.md) — Container bootstrap and state persistence · docker-entrypoint.sh
- [context7-docs-cli](context7-docs-cli.md) — Context7 docs CLI · scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
- [cost-budget-calibration](cost-budget-calibration.md) — Cost & budget calibration · scripts/ops/bloat-trend.py, scripts/ops/budget-calibration-report.py, scripts/ops/cost-audit.py, scripts/ops/operator-usage-report.sh
- [dashboard-browser-cockpit](dashboard-browser-cockpit.md) — Dashboard browser cockpit · dashboard/app.js
- [dashboard-server](dashboard-server.md) — Dashboard server · dashboard/sentry_client.py, dashboard/server.py
- [directive-writer-and-promotion-gate](directive-writer-and-promotion-gate.md) — Directive writer and promotion gate · scripts/analyst/promote_directive.py, scripts/core/directive_writer.py
- [docker-host-disk-guard](docker-host-disk-guard.md) — Docker & host disk guard · scripts/ops/docker-prune-safe.sh
- [engine-usage-cost-adapter](engine-usage-cost-adapter.md) — Engine usage cost adapter · scripts/core/engine-usage-cost.py
- [fail-closed-verification-invariant](fail-closed-verification-invariant.md) — Fail-closed verification invariant · scripts/core/jcode-mcp-probe.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [headinspect-header-inspector](headinspect-header-inspector.md) — HeadInspect header inspector · projects/headinspect/migrations/0001_hits.sql, projects/headinspect/src/index.ts, projects/headinspect/src/inspect.ts, projects/headinspect/src/render.ts
- [jcode-event-stream-utilities](jcode-event-stream-utilities.md) — jcode event-stream utilities · scripts/core/jcode-final-text.py, scripts/ops/context7-check.py, scripts/ops/tool-usage-audit.py, scripts/ops/turn-audit.py
- [jcode-mcp-config-probe](jcode-mcp-config-probe.md) — jcode MCP config & probe · scripts/core/jcode-mcp-config.py, scripts/core/jcode-mcp-probe.py, scripts/ops/verify-mcp-keys.py
- [jcode-pilot-acceptance-smoke-test](jcode-pilot-acceptance-smoke-test.md) — jcode pilot acceptance smoke test · scripts/analyst/jcode-pilot-smoke.sh
- [ki-k-linear-workstream-tooling](ki-k-linear-workstream-tooling.md) — KİK & Linear workstream tooling · scripts/ops/kik-decision-read.py, scripts/ops/linear-track.py
- [loop-lifecycle-monitoring](loop-lifecycle-monitoring.md) — Loop lifecycle & monitoring · scripts/core/monitor.sh, scripts/core/sentry-heartbeat.sh, scripts/core/stop-loop.sh, scripts/linux/noop-action.sh, scripts/linux/status-linux.sh, scripts/macos/install-daemon.sh, scripts/macos/status-mac.sh
- [operator-escalation-notification](operator-escalation-notification.md) — Operator escalation & notification · scripts/core/operator_request_notify.py, scripts/core/telegram-notify.sh, scripts/ops/directive-staleness-watch.py, scripts/ops/registry-queue-watch.py, scripts/ops/reply-watch.py
- [opportunity-analyst-cron](opportunity-analyst-cron.md) — Opportunity Analyst cron · scripts/ops/opportunity-analyst-cron.sh
- [opportunity-analyst-pipeline](opportunity-analyst-pipeline.md) — Opportunity Analyst pipeline · scripts/analyst/merge_registry.py, scripts/analyst/opportunity-analyst-jcode.sh, scripts/analyst/opportunity-analyst.sh, scripts/analyst/promote_directive.py
- [outreach-eligibility-g4-verification](outreach-eligibility-g4-verification.md) — Outreach eligibility & G4 verification · scripts/ops/g4-check.py, scripts/ops/send-gate.py, scripts/ops/site-contact-evidence.py
- [registry-directive-hygiene](registry-directive-hygiene.md) — Registry & directive hygiene · scripts/ops/directive-rule-sweep.py, scripts/ops/extract-axis-evidence.py, scripts/ops/registry-archive.py
- [secret-handling-discipline](secret-handling-discipline.md) — Secret handling discipline · scripts/core/jcode-mcp-config.py, scripts/ops/airtable-read.py, scripts/ops/airtable-write.py, scripts/ops/docker-prune-safe.sh, scripts/ops/linear-track.py, scripts/ops/verify-mcp-keys.py
- [session-hygiene-and-context-window-guards](session-hygiene-and-context-window-guards.md) — Session hygiene and context-window guards · scripts/compact-preflight.py, scripts/context-watch.py
- [snapog-cost-alerting-cron](snapog-cost-alerting-cron.md) — SnapOG cost-alerting cron · projects/_archive/snapog/src/alerts/check.ts, projects/_archive/snapog/src/alerts/graphql.ts, projects/_archive/snapog/src/alerts/index.ts, projects/_archive/snapog/src/alerts/thresholds.ts, projects/_archive/snapog/src/alerts/webhook.ts
- [snapog-d1-schema](snapog-d1-schema.md) — SnapOG D1 schema · projects/_archive/snapog/migrations/0001_init.sql, projects/_archive/snapog/migrations/0002_waitlist.sql, projects/_archive/snapog/migrations/0003_cache_key_tracking.sql
- [snapog-north-star-metric-wap](snapog-north-star-metric-wap.md) — SnapOG north-star metric (WAP) · docs/operations/north-star-metric-query.sql
- [snapog-og-image-service](snapog-og-image-service.md) — SnapOG OG image service · projects/_archive/snapog/src/dashboard/pages.ts, projects/_archive/snapog/src/index.ts, projects/_archive/snapog/src/og/render.ts, projects/_archive/snapog/src/og/templates.ts, projects/_archive/snapog/src/types.ts
- [snapog-operational-smoke-tests](snapog-operational-smoke-tests.md) — SnapOG operational smoke tests · projects/_archive/snapog/sample/alerts-dry-run.sh, projects/_archive/snapog/sample/cache-cap-test.sh, projects/_archive/snapog/sample/smoke-test.sh
- [snapog-waitlist-capture](snapog-waitlist-capture.md) — SnapOG waitlist capture · projects/_archive/snapog-landing/functions/api/waitlist.ts
- [state-snapshot-idle-skip-audit-trail](state-snapshot-idle-skip-audit-trail.md) — State snapshot & idle-skip audit trail · scripts/ops/idle-skip-note.py, scripts/ops/state-snapshot.py
- [turn-audit-policy-script](turn-audit-policy-script.md) — turn-audit policy script · scripts/ops/turn-audit.py
- [turn-audit-regression-suite](turn-audit-regression-suite.md) — turn-audit regression suite · tests/test_turn_audit.sh
- [value-sensitive-leak-scanning](value-sensitive-leak-scanning.md) — Value-sensitive leak scanning · scripts/core/bridge_leak_scan.py

## Files

61 per-file wiring cards mirror the source tree under `graft/` (59 carry extracted symbols). They are deliberately not enumerated here —
`grep` a symbol or `find`/`ls` a filename under `graft/` to land on the card for that file.
