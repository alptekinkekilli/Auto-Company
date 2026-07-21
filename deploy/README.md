# Deploying Auto-Company on Coolify (Hetzner, shared host)

Runs the **dashboard + autonomous loop** in one container. Target: `linux/amd64`.
The host is shared (3.7 GB RAM), so keep this app on a **tight memory limit** and
avoid concurrent builds.

## 1. Coolify application

- Coolify: **Cloud** (app.coolify.io), server uuid `i4v4rns6j4cj8r4guu2rut3u`.
- Create a **separate project** (don't mix with `powerupp/production`).
- Add application → source `alptekinkekilli/Auto-Company`, branch `feat/deploy-container`.
- Build pack: **Dockerfile**.
- Port: **8787** (Traefik routes the domain to this).
- Domain: `deck.appricode.tr` (grey-cloud first for Let's Encrypt; orange once Cloudflare Access is on).

## 2. Resource limits (shared host — important)

- Memory limit: **~1.5 GB** (hard), so it can't starve `powerupp` / `commonly-miniapp`.
- CPU: leave shared; the 4 GB swap is the backstop.
- Do **not** run other builds while this one builds.

## 3. Environment variables

| Var | Type | Value / note |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | **secret** | Output of `claude setup-token`. Headless auth for the loop. |
| `GH_TOKEN` | **secret** | The company's GitHub PAT (`repo` + `workflow`). Used by `gh` + git push. |
| `COMPANY_GIT_NAME` | plain | The company's own git author name (not your personal identity). |
| `COMPANY_GIT_EMAIL` | plain | The company's own git email. |
| `DASHBOARD_PORT` | plain | `8787` (matches Coolify port). |
| `LOOP_INTERVAL` | plain | Seconds between cycles (default `30`; raise to reduce load). |
| `MODEL` | plain | Optional model override; empty = engine default. |

> Auth env var: `claude setup-token` produces a long-lived token consumed via
> `CLAUDE_CODE_OAUTH_TOKEN`. Confirm the exact variable name against the installed
> CLI version on first deploy.

Secrets never live in the repo. Locally they sit in macOS Keychain
(`~/projects/autocompany-deploy/secrets/`); in Coolify they are encrypted env vars.

## 4. Persistent storage (Coolify → Storages)

Map these so work survives redeploys:

- `/app/memories` — consensus + human-directive
- `/app/projects` — the company's built projects
- `/app/logs` — cycle logs

## 5. Health check

- `GET /api/status` → HTTP 200.

## 6. Notes

- Dashboard Start/Stop buttons are **no-ops** in container mode (the loop is the
  container's main process). Stop/restart via Coolify.
- The Director panel writes `memories/human-directive.md`; the loop reads it each
  cycle (top-priority Next Action), then marks it DONE.
- Access to the dashboard is gated by **Cloudflare Access OTP** (Phase 5); admin/SSH
  to the host is via **Tailscale**.
