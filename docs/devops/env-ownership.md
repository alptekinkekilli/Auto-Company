# Environment ownership — which store owns which key

There are **two** config stores, not three. The cockpit Settings panel is not a store: it
writes `logs/runtime.env` (`dashboard/server.py`, `write_settings`). What looks like a third
layer is a second editor for the second store.

| Store | Lives in | Written by | Reaches the loop |
|---|---|---|---|
| Coolify env UI | the container environment, fixed at boot | operator via Coolify, or the Coolify API with an admin-scoped token | directly, as PID 1's env |
| `logs/runtime.env` | a persistent volume, survives redeploys | cockpit Settings panel, or an SSH append | `docker-entrypoint.sh` exports each key at boot |

**Precedence: `runtime.env` wins.** The entrypoint parses it after the container env exists
and re-exports every key, so a key set in both places takes the `runtime.env` value and the
Coolify UI goes on displaying a value that does nothing. Since 2026-07-28 the entrypoint
prints one line at boot naming every shadowed key (names only — never values), so this is
visible in the deploy log instead of being inferred from behaviour.

## The rule

**One owner per key.**

- **Coolify owns** what the container cannot boot without and what never changes at runtime:
  `CLAUDE_CODE_OAUTH_TOKEN`, `CODEX_AUTH_B64`, `GH_TOKEN`, `CLOUDFLARE_API_TOKEN`,
  `CLOUDFLARE_ACCOUNT_ID`, `CONTEXT7_API_KEY`, `COMPANY_GIT_NAME`, `COMPANY_GIT_EMAIL`,
  `DASHBOARD_PORT`.
- **`runtime.env` owns** every operator-tunable knob and every API key the company acquires
  over its life: the router/budget/ladder knobs, `DISCOVERY_ENABLED`, `ESCALATE_NEXT_CYCLE`,
  the Linear/Airtable/Telegram/Stripe/Twilio/Sentry/Coolify credentials.

## Why secrets are NOT consolidated into Coolify

An earlier version of this plan proposed moving every secret to Coolify on the theory that
Coolify is the secret store. Checked against the live API on 2026-07-28: **every one of the
14 Coolify entries has `is_secret: false`**, including `CLAUDE_CODE_OAUTH_TOKEN`, `GH_TOKEN`
and `CLOUDFLARE_API_TOKEN`. Coolify is holding them as plain environment values, exactly as
`runtime.env` does. Moving credentials there would buy no protection, would break the
standing arrangement that these keys are injected without involving the operator, and would
put them somewhere the cockpit cannot reach. The split above is by **change frequency and
who edits it**, which is the distinction that actually exists.

Secrets are still never printed: the entrypoint's override report emits key names only, and
the cockpit's `SETTINGS_SPEC` whitelist means the panel can only ever write knobs.

## Drift found and cleared, 2026-07-28

Three keys were set in both stores, and every Coolify value disagreed with the live one:
`LOOP_INTERVAL` 3600 vs 900, `WINDOW_BUDGET_USD` 8 vs 40, `ROUTER_ALTERNATE` 0 vs 1. Read
together with a stale `MODEL`, the Coolify panel described a different company than the one
running — hourly cycles on an $8 budget with no engine alternation.

The production copies of those three were deleted from Coolify (values and env uuids
recorded in `autocompany-deploy/coolify-env-backup-2026-07-28.md`). Behaviour did not
change: `runtime.env` already supplied all three and already won. The shadow set is now
empty, and the boot report is what will catch the next one.

**Still outstanding, deliberately.** `MODEL` (`claude-haiku-4-5-20251001`) and
`CLAUDE_EFFORT` (`low`) remain in Coolify. They are stale in the same way —
`CLAUDE_TIER_LADDER` supersedes both on every cycle — but they are absent from
`runtime.env`, so deleting them WOULD change the inherited default rather than just tidy the
display. Moving them means writing them into `runtime.env` first, which is a two-step worth
doing on purpose rather than as a cleanup. The `is_preview=true` copies of the deleted three
also remain; they belong to preview deployments, not the running app.
