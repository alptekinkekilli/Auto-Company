# Auto-Company — Self-Host Handoff Guide

Stand up your **own** independent instance of Auto-Company on **your own** Hetzner
server + Coolify, matching the current version. Nothing here depends on the
previous operator's accounts — you provide your own everywhere.

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
- **Telegram** bot token + chat id — the per-cycle operator ping.
- **Twilio** — only if you run email/SMS outreach.
- **Cloudflare** API token — the company deploys its *products* to Cloudflare Pages/Workers.
- A payment provider (iyzico/Stripe/…) — only when you actually sell something.

---

## 2. Get the code

1. **Fork / clone** this repo into your GitHub account (e.g. `puratu1/Auto-Company`).
2. **Branch:** the current live version is on **`feat/deploy-container`**. Either
   deploy that branch, or (cleaner) merge it into `main` and deploy `main`. Whatever
   you pick, point Coolify at the branch that has this `HANDOFF.md`.
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
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | per-cycle operator ping |
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
