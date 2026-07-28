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

## Known drift, 2026-07-28

Shadowed (set in both, `runtime.env` in effect): `LOOP_INTERVAL`, `ROUTER_ALTERNATE`,
`WINDOW_BUDGET_USD`. The Coolify copy of `LOOP_INTERVAL` disagrees with the live value.

Stale in Coolify and owned by `runtime.env` per the rule above, but not yet moved:
`MODEL` (still `claude-haiku-4-5-20251001`, superseded by `CLAUDE_TIER_LADDER` on every
cycle) and `CLAUDE_EFFORT`. Removing them from Coolify changes the effective value unless
they are written into `runtime.env` first, so that is a deliberate two-step, not a cleanup
to do casually.
