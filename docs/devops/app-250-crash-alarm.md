# APP-250 — container crash-loop liveness alarm

## Problem

The Auto-Company container crash-looped twice: 2026-07-24 (~5h, `APP-235`) and
2026-07-26 (~2.5h, memory `container-crashloop-2026-07-26.md`). Both times nobody
found out until Docker's restart-manager had already retried, given up, and
**removed the container — taking the crash logs with it**. Nothing running inside
the container can report this failure mode, because the failure mode is "the whole
container is dead."

## What's built (automatic, already deployed)

1. **`scripts/core/sentry-heartbeat.sh`** — a background process started by
   `docker-entrypoint.sh` alongside the dashboard and the loop (but NOT part of
   their mutual supervision — its own death does not tear the container down).
   Every 90s it POSTs a check-in to a Sentry Crons monitor
   (`auto-company-container-heartbeat`, project `appricode/node-cloudflare-workers`)
   using `SENTRY_DSN` from `runtime.env`. The monitor is configured (via
   `monitor_config` upsert on first check-in) with a 2-minute expected interval and
   2-minute margin — so if the container dies, Sentry flags it "missed" within
   **~4 minutes**, not ~2.5 hours.
2. **Cloudflare Worker `autocompany-crash-alert-relay`**
   (`~/projects/autocompany-crash-alert-relay`, sibling repo like
   `autocompany-outreach-cron` — NOT inside this repo's `projects/`, since it's
   internal infra, not a company product) —
   `https://autocompany-crash-alert-relay.akekilli.workers.dev/sentry-webhook`.
   Receives a Sentry alert-rule webhook, relays a formatted message to the
   existing Telegram bot (`TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, same ones
   `telegram-notify.sh` uses). Verified end-to-end with a synthetic payload — Worker
   returned `relayed`/200, and a direct `sendMessage` call to the same chat_id
   independently confirmed the bot/chat pairing works.
   Deployed via `wrangler` with the `autocompany-cf-workers-token` Keychain secret,
   account `6d289265fe41b9d64ca0d38fddfee6c5` (same account as the other company
   Workers).

## The integration + alert rule — now done via API (2026-07-27), not the UI

Originally this required a manual Sentry UI step, because the Sentry MCP tools
available in-session only exposed read/find operations for alert rules and
integrations (no `create_integration`/`create_alert_rule` tool). That's still true
for the MCP — but a **personal Sentry auth token** (scopes: `org:admin`,
`org:write`, `org:read`, `project:write`, `project:read`, `alerts:write`; Keychain
`autocompany-sentry-api-token`, exported as `SENTRY_AUTH_TOKEN` in `~/.zshrc`) plus
the official `sentry` CLI (`cli.sentry.dev`, installed to `~/.local/bin/sentry`)
made it possible to do the whole thing via API instead:

1. **Internal integration** created via `POST /sentry-apps/` (org-agnostic path,
   organization passed in the body — the org-scoped
   `/organizations/{org}/sentry-apps/` path only supports GET). This endpoint is
   **not in Sentry's documented/public OpenAPI schema** (confirmed by checking both
   the schema directly and `sentry schema sentry-apps`, which only lists
   GET/PUT/DELETE) — it works, but treat it as unstable/undocumented if it ever
   needs to be recreated. Body: `{name, organization, author, webhookUrl,
   isAlertable: true, isInternal: true, verifyInstall: false, scopes: [],
   events: []}`. Result: slug `autocompany-crash-alert-relay-fda74a`, uuid
   `58e5b06d-3201-4288-b229-e472a06ec7a7`, auto-installed on the org
   (`status: installed` confirmed via `/sentry-app-installations/`).
2. **Alert rule** created via `POST /projects/appricode/node-cloudflare-workers/rules/`
   (also not in the documented schema — same caveat). Rule ID `722786`, name
   "Crash-loop heartbeat missed check-in", `actionMatch: any`, conditions =
   `FirstSeenEventCondition` (a new issue is created) + `RegressionEventCondition`
   (issue goes resolved → unresolved), action =
   `sentry.rules.actions.notify_event_service.NotifyEventServiceAction` with
   `service: autocompany-crash-alert-relay-fda74a`. **Scope note:** this fires on
   ANY new/regressed issue in the project, not narrowly scoped to just the Crons
   monitor's missed-checkin issue type — the project also receives the cockpit's
   own Sentry error reports (`sentry-cockpit-monitoring.md`, same DSN/project), so
   this alarm will also fire for ordinary app errors. Treated as acceptable (more
   signal, not noise, for a company this size) rather than narrowed further.
3. **Worker hardening applied**: the integration's `clientSecret` was fetched
   (`GET /sentry-apps/{slug}/`) and set as the Worker's `SENTRY_WEBHOOK_SECRET`
   (`wrangler secret put`) — previously unset, so the `sentry-hook-signature` HMAC
   check in `src/index.js` was silently skipped. It's now enforced.

**End-to-end verification (real, not assumed):** two synthetic events were sent via
`sentry event send` (unique fingerprints, so each was a genuinely new issue). The
first (`NODE-CLOUDFLARE-WORKERS-2`) updated the rule's `Last Triggered` timestamp
but the webhook never reached the Worker (checked via live `wrangler tail` —
nothing arrived; root cause not found, possibly a propagation delay right after
creating a brand-new integration). The second, ~6 minutes later
(`NODE-CLOUDFLARE-WORKERS-3`), worked cleanly end to end: issue created → rule
fired (`Last Triggered` updated again) → `wrangler tail` showed `POST
.../sentry-webhook - Ok` → Worker returned 200 (which only happens after a
successful Telegram send; a Telegram failure returns 502). Both test issues were
resolved afterward to keep the project clean.

**Residual gap, not yet tested:** verification used synthetic *error* events, not
an actual missed Crons check-in. A real missed check-in should create an issue the
same way (Sentry unified Crons/Monitor failures into the regular issue platform),
so this is expected to work identically, but the gold-standard test — stopping
`sentry-heartbeat.sh` in a real container and confirming a Telegram message arrives
within ~5 minutes — has not been run.

## What this still does NOT solve

Even with the alarm live, **actually capturing the crash-loop's `docker logs`
before Docker's restart-manager removes the container still requires a human (or a
separate host-side script) to react and run `docker logs <container> --tail 2000
> evidence.log` promptly** after the Telegram alert arrives. Sentry and the
Cloudflare Worker have no SSH/Docker access to the Hetzner host and cannot capture
that automatically. A ~4-minute alert gives a real window to do this manually
(the 2026-07-26 incident ran for 2.5 hours before removal), but it is not yet a
fully automatic capture. Flagged as a possible follow-up, not built here.
