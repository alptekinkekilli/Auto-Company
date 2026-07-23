# Phase-6 Operator Runbook — Auto-Company on Hetzner/Coolify

**Audience:** the human operator. **Scope:** start/stop, redeploy, rollback, secret rotation, sending a directive, health checks.
Companion to [APP-181](https://linear.app/appricode/issue/APP-181). All destructive actions respect the guardrails in `CLAUDE.md` (never delete repos/CF projects, never touch the original `appricode-panel`, never force-push protected branches).

---

## 0. System map

The company runs as **one Coolify Cloud application** (not on the operator's Mac anymore).

- **Host:** Hetzner box, reachable via `ssh powerupp-ts` (Tailscale).
- **Coolify:** Cloud (`app.coolify.io`), app UUID **`z12a992i3ty202zezspij2fn`**. Deploys the fork `alptekinkekilli/Auto-Company`, branch **`feat/deploy-container`** (auto-deploy OFF — deploys are manual).
- **Container** name: `z12a992…-<deployHash>` (the hash changes every deploy). Process tree:
  ```
  tini (pid1) → docker-entrypoint.sh (bash) → ├─ python3 dashboard/server.py --port 8787   (cockpit)
                                              └─ bash scripts/core/auto-loop.sh             (the loop)
  ```
- **Cockpit:** `https://cockpit.appricode.tr` — behind Cloudflare Access OTP (login: akekilli@gmail.com). Direct-origin bypass is closed (Traefik `cf-only` + Access).
- **Persistent volumes:** `/app/memories`, `/app/projects`, `/app/logs` survive redeploys. Host cron `docker-prune-safe` frees disk (never touches volumes).

**Key paths (in container):**
| Path | What |
|------|------|
| `/app/logs/auto-loop.log` | Loop cycle log (START / OK / WAIT Sleeping) |
| `/app/logs/runtime.env` | Operator runtime overrides (LOOP_INTERVAL, tier ladders, Coolify + Twilio secrets) |
| `/app/memories/consensus.md` | Cross-cycle baton |
| `/app/memories/human-directive.md` | The directive the loop reads first each cycle |

---

## 1. Start / Stop

The loop is a **child of the container entrypoint, supervised by Coolify** — it is *not* independently start/stoppable from inside. The cockpit Start/Stop buttons are **disabled on the container** (`hostKind=linux`) by design (APP-203); they were Mac-only.

- **Stop the company:** Coolify → application → **Stop**. (Container down; volumes preserved.)
- **Start the company:** Coolify → application → **Start**, or trigger a **Redeploy** (§2).
- **Restart everything:** a Redeploy (§2) brings up a fresh container running both the dashboard and the loop.

> There is no supported "pause just the loop without redeploy." To change loop cadence instead of stopping, edit `LOOP_INTERVAL` (§5 pattern for runtime.env) — takes effect next container start.

---

## 2. Redeploy (manual — auto-deploy is OFF)

**Golden rule: redeploy only while the loop is SLEEPING**, so no active cycle is lost.

1. **Confirm the sleep window** (verify against the system, not memory):
   ```bash
   ssh powerupp-ts 'C=$(docker ps --format "{{.Names}}" | grep "^z12a992" | head -1); docker exec "$C" sh -lc "tail -5 /app/logs/auto-loop.log"'
   ```
   Look for `[WAIT] Sleeping 900s before next cycle...` (no `[START]` after it). That gives a ~15-min window.

2. **Fire the deploy** (browser UA is REQUIRED — plain curl/urllib UA gets Cloudflare `error code: 1010`):
   ```bash
   T=$(security find-generic-password -w -a "$(whoami)" -s autocompany-coolify-deploy)
   curl -s -X POST -H "Authorization: Bearer $T" -H "User-Agent: Mozilla/5.0" \
     "https://app.coolify.io/api/v1/deploy?uuid=z12a992i3ty202zezspij2fn"
   ```
   Expect HTTP 200 + `deployment queued`. (`autocompany-coolify-deploy` is deploy-scoped: POST /deploy only, 403 on reads — that's normal.)

3. **Verify it landed** (new container hash + dashboard live):
   ```bash
   ssh powerupp-ts 'C=$(docker ps --format "{{.Names}}" | grep "^z12a992" | head -1); echo "$C"; docker exec "$C" sh -lc "python3 -c \"import urllib.request,json;print(json.load(urllib.request.urlopen(\\\"http://localhost:8787/api/ideas\\\")).get(\\\"present\\\"))\""'
   ```
   `True` = dashboard serving. Also confirm the container hash changed.

> Cockpit "Save & Redeploy" button: works once `COOLIFY_URL=https://app.coolify.io` is set in runtime.env (it is); if it ever 1010s, use the CLI above.

---

## 3. Rollback

Auto-deploy is off, so "rollback" = deploy a known-good commit.

- **Forward-fix (preferred, keeps history):**
  ```bash
  cd ~/projects/autocompany
  git revert <bad-sha>            # or git revert <range>
  git push origin feat/deploy-container
  ```
  then Redeploy (§2). The build always pulls branch HEAD.
- **Coolify deployment history:** Coolify → application → **Deployments** → pick a previous successful deployment → **Redeploy**. Use when you need the old image fast and can't rebuild.
- **Never** `git push --force` to `feat/deploy-container` or `main` (guardrail).

---

## 4. Secret rotation

Two stores, kept in sync:
- **macOS Keychain** (operator's Mac): tooling + deploy secrets — `autocompany-*` items (e.g. `autocompany-coolify-deploy`, `autocompany-context7-key`, `autocompany-airtable-pat`). Managed via `~/projects/autocompany-deploy/secrets/store-secret.sh`.
- **Coolify env params** → injected into the container as env vars (visible in `/proc/1/environ`) and mirrored where needed into `/app/logs/runtime.env`.

**Rotate a secret (general pattern — e.g. the Coolify deploy token, done in APP-217):**
1. Create the new secret in the provider; **revoke the old one only after the new one is validated.**
2. Store new value locally: `~/projects/autocompany-deploy/secrets/store-secret.sh <name> ` (updates Keychain; `-U` overwrites).
3. Update the container copy if the loop/dashboard uses it — edit `/app/logs/runtime.env` (never print the value):
   ```bash
   ssh powerupp-ts 'C=$(docker ps --format "{{.Names}}" | grep "^z12a992" | head -1); docker exec -i "$C" sh -lc "…write KEY=<newval> into /app/logs/runtime.env…"'
   ```
   …and/or update the Coolify env param (survives redeploys). runtime.env changes apply on next container start.
4. **Validate** the new secret works (e.g. a deploy POST returns 200) **before** revoking the old.
5. Revoke the old secret in the provider; delete the stale Keychain entry if replaced.

> Never commit secret values to the repo or print them in logs (guardrail). `SEND_SECRET` must never appear in DNS; `INBOUND_SECRET` is the DNS-safe one.

---

## 5. Send a directive to the company

The loop reads `/app/memories/human-directive.md` **first each cycle**. It must be in the `## Status` / `## Directive` format or the cockpit shows "none".

**Use the wrapper (do not hand-write the file):**
```bash
~/projects/autocompany-deploy/scripts/apply-directive.sh "Your directive body here…"
```
It wraps the body as `# Human Directive` / `## Status\nPENDING` / `## Directive …`, auto-detects the running container, writes the file, and verifies the cockpit shows `PENDING`. The loop flips Status to `DONE` after it applies the directive (one authorized directive per cycle, within its gates).

**Runtime override (LOOP_INTERVAL etc.):** edit `/app/logs/runtime.env` (same idea as §4 step 3); applies next container start.

---

## 6. Health checks / observability

```bash
# Loop alive + current phase
ssh powerupp-ts 'C=$(docker ps --format "{{.Names}}" | grep "^z12a992" | head -1); docker exec "$C" sh -lc "tail -12 /app/logs/auto-loop.log"'
# Dashboard endpoints (internal port 8787, not published — Traefik fronts it)
#   /api/ideas   → opportunity scan feed
#   /api/directive → current directive Status
# Cockpit (browser): https://cockpit.appricode.tr  (Cloudflare Access OTP)
```

**Gotcha:** `docker exec … sh -lc 'echo $VAR'` shows a *fresh* shell's env, NOT the entrypoint-sourced env the loop/dashboard actually run with. To read the real runtime config, read `/app/logs/runtime.env` or `/proc/1/environ`, not a fresh `echo`.

---

## 7. Guardrails (non-negotiable — see CLAUDE.md)

- No repo/CF-project deletion; no `docker volume prune` (only build-cache/image/container prune).
- Never push/PR/write to the original `alptekinkekilli/appricode-panel` — only the fork `appricode-panel-autoco`.
- WTP hard-STOP: no product code / MVP / launch until a real paid signal; the company contacts no one autonomously — a human triggers every outreach send.
- Redeploy only during a loop sleep window.
