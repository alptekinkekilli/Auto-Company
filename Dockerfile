# Auto-Company — single container running the Control Deck dashboard + the
# autonomous loop (Claude engine). Target platform: linux/amd64 (Hetzner CX23).
#
# Build:  docker build -t auto-company .
# Run:    see deploy/README.md (Coolify) — requires CLAUDE_CODE_OAUTH_TOKEN.
FROM node:22-bookworm-slim

# System deps:
#  - python3: stdlib-only dashboard server (no pip deps)
#  - git/jq/curl/ca-certificates: the loop + the company's real dev work
#  - procps: pgrep/kill used by the loop and status scripts
#  - tini: proper PID 1 / signal reaping
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 git jq curl ca-certificates procps tini gnupg gosu \
    && mkdir -p -m 755 /etc/apt/keyrings \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
         -o /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
         > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

# Claude Code CLI (the loop's engine)
RUN npm install -g @anthropic-ai/claude-code && npm cache clean --force

# Codex CLI (fallback engine when Claude is usage-limited) — 0.144.x supports gpt-5.6-sol
RUN npm install -g @openai/codex@0.144.6 && npm cache clean --force

# Wrangler — the company deploys its products to Cloudflare (Pages/Workers).
# Authenticates via CLOUDFLARE_API_TOKEN (deploy-scoped Coolify secret).
RUN npm install -g wrangler && npm cache clean --force

# ccusage — cross-agent token-cost ESTIMATE (Claude + Codex) for the cockpit Cost panel.
# Reads local transcripts only; the dashboard shells out to it (cached, background).
RUN npm install -g ccusage && npm cache clean --force

WORKDIR /app
COPY . .

RUN chmod +x scripts/core/*.sh scripts/linux/*.sh docker-entrypoint.sh 2>/dev/null || true \
    && mkdir -p memories projects logs

# Non-root user: claude refuses --dangerously-skip-permissions as root.
# The entrypoint starts as root (to fix volume perms) then drops to `app`.
# Pre-accept the workspace trust dialog so headless runs aren't blocked.
RUN useradd -m -u 10001 -s /bin/bash app \
    && printf '{"projects":{"/app":{"hasTrustDialogAccepted":true}}}\n' > /home/app/.claude.json \
    && mkdir -p /home/app/.codex \
    && printf 'model = "gpt-5.6-sol"\nmodel_reasoning_effort = "low"\napproval_policy = "never"\n' > /home/app/.codex/config.toml \
    && chown -R app:app /app /home/app

# Persisted across redeploys (map these in Coolify → Persistent Storage)
VOLUME ["/app/memories", "/app/projects", "/app/logs"]

ENV ENGINE=claude \
    CLAUDE_PERMISSION_MODE=bypassPermissions \
    CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 \
    DASHBOARD_PORT=8787 \
    LOOP_INTERVAL=30

EXPOSE 8787

ENTRYPOINT ["/usr/bin/tini", "--", "/app/docker-entrypoint.sh"]
