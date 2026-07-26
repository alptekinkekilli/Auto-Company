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

## What's NOT automatic — one manual step in the Sentry UI

Sentry's alert-rule "send a webhook" action requires a **Custom (Internal)
Integration**, which cannot be created via the Sentry MCP tools available to this
session (no `create_integration`/`create_alert_rule` tool was exposed — only
read/find tools for alert rules, and read/find/get for monitors). This has to be
done once, by hand, in the Sentry web UI:

1. **Settings → Developer Settings → Custom Integrations → Create New Integration
   → Internal Integration.**
   - Name: `autocompany-crash-alert-relay` (or similar).
   - Webhook URL: `https://autocompany-crash-alert-relay.akekilli.workers.dev/sentry-webhook`
   - Under **Alert Rule Action**, check the box that lets this integration be used
     as an alert action (label varies by Sentry version — look for "Enable
     Alert Rule Action" / "This integration can create alerts").
   - Save. Sentry will show a **Client Secret** — copy it.
2. **(Optional, hardening) Set the Worker's `SENTRY_WEBHOOK_SECRET`** to that
   Client Secret so the Worker verifies the `sentry-hook-signature` header instead
   of accepting any POST to that URL unauthenticated:
   ```bash
   cd ~/projects/autocompany-crash-alert-relay
   printf '%s' '<client secret>' | wrangler secret put SENTRY_WEBHOOK_SECRET
   ```
   Without this the endpoint still works (signature check is skipped when the var
   is unset) — it's a hardening step, not a blocker for the alarm to function.
3. **Alerts → Create Alert → Crons monitor → Alert conditions**: select the
   `auto-company-container-heartbeat` monitor, condition = monitor becomes
   unhealthy / missed check-in (exact wording depends on Sentry version), action =
   "Send a notification via `autocompany-crash-alert-relay`" (the internal
   integration from step 1). Save.

Once this is done: container dies → ~4 min → Sentry marks the monitor missed →
alert rule fires → Worker relays to Telegram. Verify by stopping the heartbeat
process manually in a test container (`docker exec <c> pkill -f sentry-heartbeat`)
and confirming a Telegram message arrives within ~5 minutes.

## What this still does NOT solve

Even with the alarm live, **actually capturing the crash-loop's `docker logs`
before Docker's restart-manager removes the container still requires a human (or a
separate host-side script) to react and run `docker logs <container> --tail 2000
> evidence.log` promptly** after the Telegram alert arrives. Sentry and the
Cloudflare Worker have no SSH/Docker access to the Hetzner host and cannot capture
that automatically. A ~4-minute alert gives a real window to do this manually
(the 2026-07-26 incident ran for 2.5 hours before removal), but it is not yet a
fully automatic capture. Flagged as a possible follow-up, not built here.
