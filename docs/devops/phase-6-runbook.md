# Operator Runbook — Auto-Company on Hetzner/Coolify

**Audience:** the human operator. **Scope:** start/stop, redeploy, rollback, secret
rotation, sending a directive, health checks.
All destructive actions respect the guardrails in `CLAUDE.md` (never delete repos/CF
projects, never write the human dev's ORIGINAL mirrored repo, never force-push
protected branches). New-operator setup: see `HANDOFF.md`.

> **Fill in your own values** where you see `<...>`:
> `<SSH_HOST>` your server's SSH alias · `<COOLIFY_APP_UUID>` your Coolify app uuid
> · `<APP_UUID_PREFIX>` first chars of the container name (= your app uuid) ·
> `<COCKPIT_URL>` your dashboard URL · `<ACCESS_EMAIL>` your access login ·
> `<GITHUB>/Auto-Company` your fork · `<DEPLOY_BRANCH>` the branch Coolify builds ·
> `<secret-store>` your local secret store (e.g. `~/projects/autocompany-deploy/secrets`).

---

## 0. System map

The company runs as **one Coolify application** (not on the operator's laptop).

- **Host:** your Docker host (e.g. Hetzner box), reachable via `ssh <SSH_HOST>`.
- **Coolify:** app UUID **`<COOLIFY_APP_UUID>`**. Deploys your fork
  `<GITHUB>/Auto-Company`, branch **`<DEPLOY_BRANCH>`** (auto-deploy OFF — deploys are manual).
- **Container** name: `<APP_UUID_PREFIX>…-<deployHash>` (the hash changes every deploy). Process tree:
  ```
  tini (pid1) → docker-entrypoint.sh (bash) → ├─ python3 dashboard/server.py --port 8787   (cockpit)
                                              └─ bash scripts/core/auto-loop.sh             (the loop)
  ```
- **Cockpit:** `<COCKPIT_URL>` — put it behind an access layer (Cloudflare Access /
  Tailscale); do not leave it public. (Example: Cloudflare Access OTP, login `<ACCESS_EMAIL>`.)
- **Persistent volumes:** `/app/memories`, `/app/projects`, `/app/logs` survive redeploys.
  A host prune cron may free disk — it must never touch these volumes.

**Key paths (in container):**
| Path | What |
|------|------|
| `/app/logs/auto-loop.log` | Loop cycle log (START / OK / WAIT Sleeping) |
| `/app/logs/runtime.env` | Operator runtime overrides (LOOP_INTERVAL, tier ladders, secrets) |
| `/app/memories/consensus.md` | Cross-cycle baton |
| `/app/memories/human-directive.md` | The directive the loop reads first each cycle |

---

## 1. Start / Stop

The loop is a **child of the container entrypoint, supervised by Coolify** — it is
*not* independently start/stoppable from inside. The cockpit Start/Stop buttons are
**disabled on the container** (`hostKind=linux`) by design; they were laptop-only.

- **Stop the company:** Coolify → application → **Stop**. (Container down; volumes preserved.)
- **Start the company:** Coolify → application → **Start**, or trigger a **Redeploy** (§2).
- **Restart everything:** a Redeploy (§2) brings up a fresh container running both the dashboard and the loop.

> There is no "pause just the loop without redeploy." To change loop cadence instead
> of stopping, edit `LOOP_INTERVAL` (§5) — takes effect next container start.

---

## 2. Redeploy (manual — auto-deploy is OFF)

**Golden rule: redeploy only while the loop is SLEEPING**, so no active cycle is lost.

1. **Confirm the sleep window** (verify against the system, not memory):
   ```bash
   ssh <SSH_HOST> 'C=$(docker ps --format "{{.Names}}" | grep "^<APP_UUID_PREFIX>" | head -1); docker exec "$C" sh -lc "tail -5 /app/logs/auto-loop.log"'
   ```
   Look for `[WAIT] Sleeping … before next cycle` (no `[START]` after it). That gives your inter-cycle window.

2. **Fire the deploy** (a browser User-Agent is REQUIRED if your Coolify is behind
   Cloudflare — a plain curl/urllib UA can get Cloudflare `error code: 1010`):
   ```bash
   T=$(security find-generic-password -w -a "$(whoami)" -s <secret-store-coolify-deploy-token>)
   curl -s -X POST -H "Authorization: Bearer $T" -H "User-Agent: Mozilla/5.0" \
     "$COOLIFY_URL/api/v1/deploy?uuid=<COOLIFY_APP_UUID>"
   ```
   Expect HTTP 200 + `deployment queued`. (A deploy-scoped token is POST /deploy only; 403 on reads is normal.)

3. **Verify it landed** (new container hash + dashboard live):
   ```bash
   ssh <SSH_HOST> 'C=$(docker ps --format "{{.Names}}" | grep "^<APP_UUID_PREFIX>" | head -1); echo "$C"; docker exec "$C" sh -lc "curl -s -o /dev/null -w %{http_code} http://localhost:8787/api/status"'
   ```
   `200` = dashboard serving. Also confirm the container hash changed.

> Cockpit "Save & Redeploy" button: works once `COOLIFY_URL` is set in runtime.env;
> if it ever hits a Cloudflare 1010, use the CLI above.

---

## 3. Rollback

Auto-deploy is off, so "rollback" = deploy a known-good commit.

- **Forward-fix (preferred, keeps history):**
  ```bash
  cd ~/projects/autocompany
  git revert <bad-sha>            # or git revert <range>
  git push origin <DEPLOY_BRANCH>
  ```
  then Redeploy (§2). The build always pulls branch HEAD.
- **Coolify deployment history:** Coolify → application → **Deployments** → pick a
  previous successful deployment → **Redeploy**. Use when you need the old image fast.
- **Never** `git push --force` to `<DEPLOY_BRANCH>` or `main` (guardrail).

---

## 4. Secret rotation

Two stores, kept in sync:
- **Local secret store** (operator's machine): tooling + deploy secrets (e.g. the
  Coolify deploy token, Context7 key, Airtable PAT). Managed via your secret store
  (e.g. `<secret-store>/store-secret.sh`).
- **Coolify env params** → injected into the container as env vars (visible in
  `/proc/1/environ`) and/or mirrored into `/app/logs/runtime.env`.

**Rotate a secret (general pattern):**
1. Create the new secret in the provider; **revoke the old one only after the new one is validated.**
2. Store the new value locally (updates your secret store).
3. Update the container copy if the loop/dashboard uses it — edit `/app/logs/runtime.env`
   (never print the value):
   ```bash
   ssh <SSH_HOST> 'C=$(docker ps --format "{{.Names}}" | grep "^<APP_UUID_PREFIX>" | head -1); printf "\nKEY=%s\n" "<newval>" | docker exec -i "$C" sh -c "cat >> /app/logs/runtime.env"'
   ```
   …and/or update the Coolify env param (survives redeploys). runtime.env changes apply on next container start.
4. **Validate** the new secret works (e.g. a deploy POST returns 200) **before** revoking the old.
5. Revoke the old secret; delete the stale local entry.

> Never commit secret values to the repo or print them in logs (guardrail). Read the
> real runtime env from `/app/logs/runtime.env` or `/proc/1/environ`, never a fresh `echo`.

---

## 5. Send a directive to the company

The loop reads `/app/memories/human-directive.md` **first each cycle**. It must be in
the `## Status` / `## Directive` format or the cockpit shows "none".

**Cockpit way:** Director panel → pick a template button → paste → fill `<FILL:>` → **Send Directive**.

**CLI wrapper** (do not hand-write the file):
```bash
<secret-store>/../scripts/apply-directive.sh ../directives/<template>.md   # set AC_SSH_HOST=<SSH_HOST>
```
It wraps the body as `# Human Directive` / `## Status\nPENDING` / `## Directive …`,
auto-detects the running container, writes the file, and verifies the cockpit shows
`PENDING`. The loop flips Status to `DONE` after it applies the directive.

**Runtime override (LOOP_INTERVAL etc.):** edit `/app/logs/runtime.env` (§4 step 3); applies next container start.

---

## 6. Health checks / observability

```bash
# Loop alive + current phase
ssh <SSH_HOST> 'C=$(docker ps --format "{{.Names}}" | grep "^<APP_UUID_PREFIX>" | head -1); docker exec "$C" sh -lc "tail -12 /app/logs/auto-loop.log"'
# Dashboard endpoints (internal port 8787, fronted by your reverse proxy):
#   /api/status  → health + loop state    /api/ideas → opportunity feed
#   /api/directive → current directive     /api/directive-templates → template buttons
# Cockpit (browser): <COCKPIT_URL>
```

**Gotcha:** `docker exec … sh -lc 'echo $VAR'` shows a *fresh* shell's env, NOT the
entrypoint-sourced env the loop/dashboard actually run with. Read `/app/logs/runtime.env`
or `/proc/1/environ` instead.

---

## 7. Guardrails (non-negotiable — see CLAUDE.md)

- No repo/CF-project deletion; no `docker volume prune` (only build-cache/image/container prune).
- Never push/PR/write to a mirrored project's ORIGINAL repo — only the company COPY
  (see the operator-project rule in `CLAUDE.md`).
- WTP hard-STOP: no product code / MVP / launch until a real paid signal; the company
  contacts no one autonomously — a human triggers every outreach send.
- Redeploy only during a loop sleep window.
