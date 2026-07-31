# Auto-Company — single container running the Control Deck dashboard + the
# autonomous loop (Claude engine). Target platform: linux/amd64 (Hetzner CX23).
#
# Build:  docker build -t auto-company .
# Run:    see deploy/README.md (Coolify) — requires CLAUDE_CODE_OAUTH_TOKEN.
#
# jcode-pilot branch: base bumped bookworm→trixie because the jcode binary
# needs GLIBC >= 2.39 (bookworm ships 2.36 — the hard blocker found in
# on-arastirma-sonuclari.md). Everything else is additive: claude/codex CLIs
# stay installed in parallel so a jcode failure is a one-line engine revert,
# not an image rollback.
FROM node:22-trixie-slim

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

# Document-processing tools for tender/procurement work (Word/Excel .docx/.xlsx
# text+table extraction, headless conversion of legacy .doc/.xls, OCR for
# scanned/embedded images). Deterministic parsing, no LLM API calls, no new
# services — Debian packages only, matching "boring technology first".
#  - python3-docx / python3-openpyxl / python3-pandas: read .docx/.xlsx text,
#    tables, and structured data directly in Python (no pip/PEP-668 needed).
#  - libreoffice-writer/-calc --no-install-recommends: headless `soffice
#    --convert-to` to normalize legacy .doc/.xls into modern formats first.
#  - tesseract-ocr + tesseract-ocr-tur: OCR for scanned pages or images
#    embedded in a document. The base tesseract-ocr package ships English
#    data only; tesseract-ocr-tur (Turkish) was found missing live on Cycle
#    276/277 when Teknik Şartname.pdf turned out to be a 10-page scanned
#    image PDF, not real text (`pdftotext` returned garbage — no font
#    encoding was actually recoverable, only rasterized JPEG pages existed).
#  - poppler-utils (pdftotext/pdftoppm): text extraction from real-text PDF
#    specs (the other controlling half of most tender packets — found
#    missing live on Cycle 276, where `soffice` cannot do PDF-to-text), and
#    `pdftoppm` to rasterize scanned-PDF pages to images for the tesseract
#    fallback above.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-docx python3-openpyxl python3-pandas \
        libreoffice-writer libreoffice-calc tesseract-ocr tesseract-ocr-tur \
        poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Claude Code CLI (the loop's engine)
# Pinned to the version production is proven on (2.1.220). Unpinned, a rebuild for an
# unrelated reason silently swaps the engine binary — and `LOOP_HARNESS=cli` is the
# jcode rollback path, so an untested CLI version would be what a rollback lands on.
RUN npm install -g @anthropic-ai/claude-code@2.1.220 && npm cache clean --force

# Codex CLI (fallback engine when Claude is usage-limited) — 0.144.x supports gpt-5.6-sol
RUN npm install -g @openai/codex@0.144.6 && npm cache clean --force

# Wrangler — the company deploys its products to Cloudflare (Pages/Workers).
# Authenticates via CLOUDFLARE_API_TOKEN (deploy-scoped Coolify secret).
RUN npm install -g wrangler && npm cache clean --force

# jcode CLI (https://github.com/1jehuang/jcode) — candidate single harness for
# both engines (RUNBOOK-jcode-gecis.md). Checksum-verified, version-pinned.
# The Linux tarball is a launcher script + `.bin` pair: BOTH must be kept
# side by side and the symlink must point at the launcher (runbook §1.1).
ARG JCODE_VERSION=v0.64.2
RUN set -eu; \
    cd /tmp; \
    curl -fsSLO "https://github.com/1jehuang/jcode/releases/download/${JCODE_VERSION}/jcode-linux-x86_64.tar.gz"; \
    curl -fsSLO "https://github.com/1jehuang/jcode/releases/download/${JCODE_VERSION}/SHA256SUMS"; \
    grep "jcode-linux-x86_64.tar.gz" SHA256SUMS | sha256sum -c -; \
    mkdir -p /opt/jcode; \
    tar xzf jcode-linux-x86_64.tar.gz -C /opt/jcode; \
    chmod +x /opt/jcode/*; \
    ln -s /opt/jcode/jcode-linux-x86_64 /usr/local/bin/jcode; \
    rm -f /tmp/jcode-linux-* /tmp/SHA256SUMS

# jcode runtime posture for loops (runbook §0.3): no telemetry, no auto-update
# (each call also passes --no-update), and trust for the existing Claude Code
# OAuth blob is written per-user by the entrypoint/pilot script, not baked here.
ENV JCODE_NO_TELEMETRY=1

# ccusage — cross-agent token-cost ESTIMATE (Claude + Codex) for the cockpit Cost panel.
# Reads local transcripts only; the dashboard shells out to it (cached, background).
# chown to the non-root app uid (10001): ccusage unconditionally chmods its own native
# binary on first run, which the syscall only allows the OWNER to do — without this the
# loop's `app` user hits EPERM and ccusage returns nothing.
RUN npm install -g ccusage && npm cache clean --force \
    && chown -R 10001:10001 /usr/local/lib/node_modules/ccusage

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
