# Auto-Company — Self-Host Handoff Guide

Stand up your **own** independent instance of Auto-Company on **your own** Hetzner
server + Coolify, matching the current version. Nothing here depends on the
previous operator's accounts — you provide your own everywhere.

> 📄 A single-page **visual** version of this guide is committed at
> [`docs/handoff.html`](docs/handoff.html) — open it in a browser for the same
> content (setup · steering · troubleshooting) laid out as a shareable page.

> **What Auto-Company is:** one Docker container that runs (1) a **dashboard**
> ("cockpit", port 8787) and (2) an **autonomous loop** (`scripts/core/auto-loop.sh`).
> Each cycle the loop runs a headless AI coding agent (`claude -p`, or the Codex CLI
> on fallback) over this repo, reading `PROMPT.md` + `CLAUDE.md` + `memories/consensus.md`
> + `memories/human-directive.md`, forming a 3–5 agent squad, doing work, and updating
> consensus. You steer it only by writing a **human directive** (via the cockpit or
> `apply-directive.sh`); everything else is autonomous. See `README.md` and
> `deploy/README.md` for deeper background.

---

## 0. Architecture at a glance

```
Coolify (your instance)  → builds the Dockerfile → runs 1 container
  container PID1 (tini) → docker-entrypoint.sh
        ├── python3 dashboard/server.py  (cockpit, :8787)
        └── scripts/core/auto-loop.sh    (the loop; engine = Claude, fallback Codex)
  persistent volumes: /app/memories  /app/projects  /app/logs
  runtime overrides:  /app/logs/runtime.env  (KEY=value, parsed by the entrypoint)
  MCP servers (.mcp.json): context7 + airtable + linear  (env-key auth)
```

---

## 1. What YOU must provide (accounts + infra)

All of these are **your own** — the previous operator's values do not carry over.

**Infrastructure**
- A **Hetzner** (or any Docker) server, `linux/amd64`, ≥ ~1.5 GB RAM free for this app.
- A **Coolify** instance (self-hosted or Cloud) pointed at that server.
- A **GitHub account** to hold your copy of this repo (fork, or have the repo
  transferred to you).
- (Optional) a **domain** for the cockpit + an access layer (Cloudflare Access /
  Tailscale) so the dashboard isn't public.

**LLM engine (required)**
- **Anthropic / Claude** subscription → run `claude setup-token` locally to get the
  headless token for `CLAUDE_CODE_OAUTH_TOKEN`. This is the one hard requirement.
- (Optional fallback) **Codex / OpenAI** → base64 your Codex `auth.json` into
  `CODEX_AUTH_B64` if you want the Codex fallback engine.

**Integrations (add the ones you use — see the full checklist in §3)**
- **Context7** API key — live library docs + the company's skill-creation.
- **Airtable** PAT + your own base — the company's CRMs/trackers.
- **Linear** API key + your own team/workspace — issue tracking.
- **Telegram** bot token + chat id — the per-cycle operator ping (setup steps: §11.1).
- **Twilio** — only if you run email/SMS outreach.
- **Cloudflare** API token — the company deploys its *products* to Cloudflare Pages/Workers.
- A payment provider (iyzico/Stripe/…) — only when you actually sell something.

---

## 2. Get the code

1. **Fork / clone** this repo into your GitHub account (e.g. `puratu1/Auto-Company`).
2. **Branch:** deploy **`main`** — it holds the full, current version (cockpit,
   framework, agents, skills, and this guide). Point Coolify at `main`.
3. The Docker build is defined by the repo's **`Dockerfile`** (node:22 + python3 +
   git/gh/jq/curl + Claude Code CLI + Codex CLI + wrangler). Coolify build pack =
   **Dockerfile**. No other build config needed.

---

## 3. Secrets & environment — complete checklist

**Source of truth:** [`logs/runtime.env.example`](logs/runtime.env.example) lists
every knob and secret with inline notes. Set values one of two ways:
- **Coolify env vars** (encrypted; recommended for secrets), OR
- copy `logs/runtime.env.example` → the container's `/app/logs/runtime.env`
  (a persistent volume) and fill it in.
Both feed the loop's environment; `runtime.env` acts as a runtime override layer.
**Never commit real secret values** — `logs/` is gitignored except the `.example`.

**Required to boot**
| Var | How to get it |
|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | `claude setup-token` on your machine (headless Claude auth) |
| `GH_TOKEN` | a GitHub PAT (`repo` + `workflow`) for the company's own commits/deploys — ideally a **separate** GitHub identity, not your personal one |
| `COMPANY_GIT_NAME` / `COMPANY_GIT_EMAIL` | the company's git author identity |

**Non-secret knobs (cockpit Settings panel edits these; defaults are fine)**
`ENGINE`, `ROUTER_ALTERNATE`, `ROUTER_TIER_LADDER`, `CLAUDE_TIER_LADDER`,
`CODEX_TIER_LADDER`, `MODEL`, `CLAUDE_EFFORT`, `CODEX_EFFORT`, `LOOP_INTERVAL`,
`WINDOW_BUDGET_USD`, `CODEX_WINDOW_LIMIT`, `BUDGET_PAUSE_SECONDS`. `DASHBOARD_PORT=8787`.

**Integrations (add as you enable each; wired in `.mcp.json` via `${VAR}`)**
| Var | For |
|---|---|
| `CONTEXT7_API_KEY` | Context7 docs MCP + skill authoring |
| `AIRTABLE_API_KEY` | Airtable MCP (base-scoped PAT to **your** base) |
| `LINEAR_API_KEY` | Linear MCP (your team) |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | per-cycle operator ping (bot/chat-id setup: §11.1) |
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_API_SID` / `TWILIO_API_SECRET` | comms/outreach |
| `CLOUDFLARE_API_TOKEN` | deploying the company's products to Cloudflare |

**Self-redeploy (optional — enables the cockpit "Save & Redeploy" + loop self-redeploy)**
| Var | For |
|---|---|
| `COOLIFY_URL` (`https://app.coolify.io` or your Coolify URL) · `COOLIFY_APP_UUID` · `COOLIFY_DEPLOY_TOKEN` | your Coolify deploy webhook |

> The MCP servers fail **open**: if a key is missing/wrong, that server simply
> exposes no tools and the loop records an access gap — it does not crash. So you
> can start with just Claude + Context7 and add Airtable/Linear/etc. later.

---

## 4. Deploy on Coolify

Follow [`deploy/README.md`](deploy/README.md) for the container mechanics, but use
**your own** values (ignore the previous operator's server uuid / repo / domain):

1. **Application** → source = *your* repo, branch = the one from §2, build pack = **Dockerfile**, port = **8787**.
2. **Memory limit** ≈ 1.5 GB (more if the box allows) so the loop has headroom.
3. **Persistent storages** (Coolify → Storages) — map all three so work survives redeploys:
   - `/app/memories` · `/app/projects` · `/app/logs`
4. **Environment variables** — from §3 (at minimum the three required ones).
5. **Health check:** `GET /api/status` → 200.
6. **Domain/access** (optional): route the domain to port 8787; gate it with
   Cloudflare Access or Tailscale — do **not** leave the cockpit public.
7. Deploy. On boot the entrypoint sources `runtime.env`, starts the dashboard, then
   the loop. First cycle runs within ~1 interval (`LOOP_INTERVAL`, default 900s).

---

## 5. Operator tooling (local, on your machine)

Optional but recommended — mirrors how the previous operator drove the company. See
`~/projects/autocompany-deploy/` in the handoff bundle (git-init'd, `secrets/` ignored):
- **Secrets store:** keep your tokens in your OS keychain (never in the repo).
- **`scripts/apply-directive.sh <body-file>`** — writes a human directive into the
  live container (`/app/memories/human-directive.md`) and verifies the cockpit shows
  it PENDING. Set `AC_SSH_HOST` to *your* server's SSH host.
- **`directives/`** — ready-to-use directive templates (Hold+Discover, Discovery,
  Un-hold+Validate, Select+Validate), each with a "Blocked / Pending Work" register.
  The cockpit also exposes these as one-click **copy buttons** in the Director panel.

You steer entirely through directives: the cockpit **Director** panel (paste a
template → fill `<FILL:>` → **Send Directive**), or `apply-directive.sh` from the CLI.

---

## 6. First-run verification

- Cockpit reachable, `GET /api/status` → 200.
- Container log shows `Auto Company Loop Started` then `Cycle #1 [START] … [OK] … [WAIT]`.
- MCP health (inside the container, loop runs under `bypassPermissions`): the loop
  reaches `context7` + `airtable` + `linear` — confirm the first cycle's consensus
  `## Execution Controls` block reads your Airtable/Linear, not "connector unavailable".
- `memories/consensus.md` updates each cycle with the `## Execution Controls` audit fields.

---

## 7. Change these for YOUR instance (important)

- **`CLAUDE.md` → Operator-project rule (appricode-panel).** It currently pins work to
  the previous operator's copy repo `alptekinkekilli/appricode-panel-autoco` and forbids
  touching the original `alptekinkekilli/appricode-panel`. If you take over that work,
  rewrite this rule to point at **your** copy repo, and keep the "never touch the human
  dev's original" principle for whatever original you're mirroring.
- **`deploy/README.md`** contains the previous operator's Coolify server uuid, repo,
  and `deck.appricode.tr` domain — replace with yours (or just rely on this HANDOFF).
- **Airtable base / Linear workspace IDs** referenced in the company's *work* (not in
  config) are the previous operator's. Your instance starts fresh: the company builds
  its own Airtable structures + Linear issues as it operates. Do **not** expect the
  previous operator's records to appear.
- **`memories/` and `projects/`** ship with the previous operator's history. Decide
  whether to keep it as seed context or clear `memories/consensus.md` +
  `memories/human-directive.md` for a clean Day-0 start (keep the guardrail docs).

---

## 8. Day-2 operations

- **Steer:** write a human directive (cockpit Director panel or `apply-directive.sh`).
  The loop treats a `PENDING` directive as top priority, then marks it `DONE`.
- **Redeploy:** only while the loop is **sleeping** (between cycles), so no active
  cycle is lost — see `docs/devops/phase-6-runbook.md`.
- **Costs:** each cycle spends real LLM tokens (Claude metered-equivalent ~a few $/cycle
  at default settings). Use `LOOP_INTERVAL`, `WINDOW_BUDGET_USD`, and the tier ladder
  to control spend. The flat Claude/Codex subscriptions are cheaper than metered for a
  24/7 loop — keep them.
- **Guardrails** (in `CLAUDE.md`, non-negotiable): no deleting GitHub repos or
  Cloudflare projects; no force-push to protected branches; no leaking secrets;
  HARD STOP — no product build before a real willingness-to-pay signal; Munger veto
  on major decisions. Keep these.

---

## 9. What does NOT transfer

The **code, prompts, framework, agents, skills, dashboard, and setup** transfer fully.
The **live business state does not**: the previous operator's Airtable base + records,
Linear workspace, Telegram bot, Cloudflare/iyzico accounts, and any active directive
are theirs. Your instance authenticates with your own keys and builds its own state
from Day 0.

> One exception worth calling out: the **Opportunity Analyst host cron** (§11.3) is
> *host-only* — like `docker-prune`, it lives on the previous operator's server, **not
> in the repo**. Its in-container parts (script, skill, panel) DO transfer; the cron
> that fires it does not. You add that yourself.

---

## 10. Troubleshooting

### 10.1 Cockpit looks primitive / behind (only Guardian·Daemon·Loop·Runtime State)
**Symptom:** the dashboard is missing the Director, Settings, Analyst, Cost, and Ideas
panels, reads `Loop: STOPPED` or "read-only dashboard".
**Two causes — fix both:**
1. **Deploy is on old code.** Coolify → app → Configuration → Git Source → Branch =
   `main` → Save → Redeploy. Build pack = **Dockerfile** (a real container, not a
   static build). Restores the full modern cockpit.
2. **Loop isn't running** (no real container / no secrets) → every panel is empty. Fix
   with 10.2.

### 10.2 Cockpit is live (200) but no cycles run
**Symptom:** the modern cockpit renders and `GET /api/status` → 200, but no cycles. The
entrypoint **hard-stops** when `CLAUDE_CODE_OAUTH_TOKEN` is absent — that is correct;
never bypass it with a dummy value.
**Cause:** the four boot secrets aren't in `runtime.env` yet (§3). Two are personal
credentials — **each instance brings its own**; never reuse another operator's tokens.

Write them **without echoing the values** — literal `KEY=value`, one per line, **no
quotes** (`GH_TOKEN=ghp_xxx`, never `"ghp_xxx"`), no trailing space/CRLF. The entrypoint
parses this file **literally — it never dot-sources it**:
```bash
umask 077
F=/app/logs/runtime.env   # or your host's mapped path, e.g. /opt/<app>-data/logs/runtime.env
cat >> "$F" <<'EOF'
COMPANY_GIT_NAME=Auto Company
COMPANY_GIT_EMAIL=bot@yourdomain
EOF
read -rs -p "CLAUDE_CODE_OAUTH_TOKEN: " T && printf 'CLAUDE_CODE_OAUTH_TOKEN=%s\n' "$T" >> "$F"; unset T; echo
read -rs -p "GH_TOKEN: " T && printf 'GH_TOKEN=%s\n' "$T" >> "$F"; unset T; echo
```
Then restart / redeploy. Verify the loop is live:
```bash
docker logs -f <container> 2>&1 | grep -E "Cycle #|\[OK\]"
```
The first `Cycle #1 … [OK]` means the loop is running and the panels start filling.

**🪟 Windows operators — where the Claude token lives.** The token is **not stored on
Windows** — Windows is only where you *generate* it (`claude setup-token` in PowerShell /
Windows Terminal; install with `npm i -g @anthropic-ai/claude-code`, or run from WSL /
Git Bash). It lives in exactly one place: the server's `runtime.env`. **Paste it into the
server shell, not a Windows file** — authoring `runtime.env` in Notepad adds `\r\n`
endings, the parser reads `token\r`, and auth fails. No backup needed: it's regenerable
(re-run `claude setup-token`); if you must keep a copy, use Windows Credential Manager.

### 10.3 `curl -I` returns 501 — not a bug
The Python server implements only `GET`, so `HEAD` (`curl -I`) returns `501`. Use
`GET /api/status` for health checks. Binding to `172.17.0.1:8787` (not public `0.0.0.0`)
is also correct — keep the cockpit behind your reverse proxy.

---

## 11. Optional add-ons

### 11.1 Telegram notifications

The company pings **you** on Telegram: an automatic one-line summary at the end of every
cycle, plus ad-hoc pings for anything time-sensitive. It's **outbound only** — the bot never
accepts commands back; you still steer entirely through the human directive (§5).

**Setup**
1. **Create a bot** — message `@BotFather` on Telegram, send `/newbot`, follow its prompts
   (name, username). It replies with a token like `123456789:AAH…` — that's
   `TELEGRAM_BOT_TOKEN`. Treat it like any other secret.
2. **Get your chat ID** — message your new bot once (anything), then open
   `https://api.telegram.org/bot<TOKEN>/getUpdates` in a browser and read `message.chat.id`
   from the JSON. Simpler shortcut: message `@userinfobot` on Telegram — it replies with your
   numeric ID directly. That number is `TELEGRAM_CHAT_ID`.
3. **Add both as env vars** — `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`, same as any other
   secret (Coolify env vars, or `runtime.env`). Fails open by design: leave either blank and
   the loop simply never sends — nothing errors, nothing blocks a cycle.

**What actually triggers a message**
| Trigger | When |
|---|---|
| Every cycle | Automatic — a one-line result + cost, no extra setup once the two env vars are set |
| 🟢 WTP signal | A real payment, pre-order, or checkout attempt settled — wants your go-ahead to deliver |
| 🛑 Blocker | Progress stopped and needs you — missing access, a directive conflict, a broken dependency |
| 🧠 Analyst | The Opportunity Analyst (§11.3) produced a pick that differs from the company's own |
| ⚠️ Guardrail | The company refused to cross a line (e.g. build-before-WTP) and wants you to resolve it |
| ⚠️ Disk | Host-level disk-usage warning from the prune cron — host-only, not in the repo |

Telegram caps messages at 4096 characters; the notifier truncates to stay under it. It never
sends secrets, tokens, or raw customer data. Implementation: `scripts/core/telegram-notify.sh`
(no-op if the two env vars are unset), wired into `scripts/core/auto-loop.sh` for the per-cycle
summary and stall warning, and callable ad-hoc via the `telegram-notify` skill.

### 11.2 Connect the Codex fallback engine
Codex is **not required** — the loop runs on Claude alone; Codex is the engine the
router fails over to when Claude hits its usage limit or the budget cap. It's a
**one-time seed**, not a per-deploy step.
1. On your own machine, produce an `auth.json`: `npm i -g @openai/codex@0.144.6` then
   `codex login` (sign in with your ChatGPT Plus/Pro) → writes `~/.codex/auth.json`.
   *(Rock-solid 24/7 alternative: put an `OPENAI_API_KEY` in `auth.json` — pay-per-use,
   never expires. The ChatGPT-sub path is cheaper but can need an occasional re-login.)*
2. base64 it and seed `CODEX_AUTH_B64` in `runtime.env`: `base64 -w0 ~/.codex/auth.json`
   (macOS: `base64 … | tr -d '\n'`), paste via the same `read -rs` method. Restart → the
   entrypoint decodes it to `CODEX_HOME=/app/logs/.codex` (on the persistent volume) and
   auto-sets `FALLBACK_ENGINE=codex`.
3. Verify in the log: `Codex auth: seeded from CODEX_AUTH_B64 (first boot)`, then
   `using persisted …/auth.json` on later restarts.

**The one trap — seed once, then leave it.** During a run Codex **rotates** its refresh
token and writes the new one back to the persisted `auth.json`. Re-injecting the original
`CODEX_AUTH_B64` on every deploy resurrects an already-used refresh token → `401 "refresh
token was already used"`. The entrypoint guards this (it never overwrites a persisted
auth), so after first boot you can even blank `CODEX_AUTH_B64`. Also seed a **freshly**
logged-in `auth.json` — one more than a few days old is already stale and 401s.

### 11.3 The Opportunity Analyst (Codex 2nd brain) cron
An independent Codex (`gpt-5.6-sol`) that reads the full scan, scores every candidate,
challenges the company's own pick, and drafts a paste-ready directive — shown in its own
cockpit panel with a Copy button. It runs **inside** the container as user `app` but a
**host cron** triggers it. A panel that reads `LOADED` with no content just means the
code is present and nothing has run yet.

**Prerequisite:** the Codex auth from 11.1 — the Analyst shares the loop's
`CODEX_HOME=/app/logs/.codex/auth.json` and aborts without it.

| Part | Transfers with the fork? |
|---|---|
| `scripts/analyst/opportunity-analyst.sh` (orchestrator) | ✅ in the image |
| Codex skill `autocompany-opportunity-director` | ✅ in the image; the script **self-installs** it into `$CODEX_HOME/skills/` on first run |
| `/api/analysis` + Analyst panel | ✅ in the image |
| **Host cron** (`opportunity-analyst-cron.sh` + `/etc/cron.d/…`) | ❌ **NOT in the repo** — add it yourself |

**Run it once, by hand** (after Codex auth is seeded and the loop is up):
```bash
C=$(docker ps --format '{{.Names}}' | grep 'auto-company' | head -1)
docker exec -u app "$C" bash /app/scripts/analyst/opportunity-analyst.sh
# ~7–10 min → the Analyst panel fills → Copy directive → paste into Director
```

**For automatic daily runs**, add a host cron. **Critical:** the Analyst and the loop's
Codex fallback share one `CODEX_HOME` — two concurrent `codex exec` runs cause a `401`,
so the cron must wait for a codex-idle window before firing:
```bash
# /usr/local/bin/opportunity-analyst-cron.sh
#!/usr/bin/env bash
set -uo pipefail
C=$(docker ps --format '{{.Names}}' | grep 'auto-company' | head -1)
[ -z "$C" ] && { echo "no container"; exit 0; }
for i in $(seq 1 25); do   # wait up to 25 min for a codex-idle window
  docker exec "$C" sh -lc "ps -eo args | grep -q '[c]odex exec'" || break
  sleep 60
done
docker exec -u app "$C" bash /app/scripts/analyst/opportunity-analyst.sh >> /var/log/opportunity-analyst.log 2>&1

# /etc/cron.d/opportunity-analyst
30 4 * * * root /usr/local/bin/opportunity-analyst-cron.sh
```
**Draft-only by design:** the Analyst never applies its own directive (it
snapshots/restores `human-directive.md`); you copy the `## Directive` block into the
Director yourself. Registry writes are additive — Archived is never silently deleted.
