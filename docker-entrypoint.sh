#!/usr/bin/env bash
# Auto-Company container entrypoint: runs the dashboard + the autonomous loop
# together, wired so the container exits (and Coolify restarts) if either dies.
set -euo pipefail
cd /app

# --- privilege drop ---------------------------------------------------------
# tini launches us as root (PID 1). claude refuses --dangerously-skip-permissions
# as root, so we fix the mounted-volume ownership here (needs root) then re-exec
# this same script as the non-root `app` user.
if [ "$(id -u)" = "0" ]; then
    mkdir -p memories projects logs
    chown -R app:app memories projects logs 2>/dev/null || true
    exec gosu app "$0" "$@"
fi

# --- from here on we run as `app` (non-root) ---
export HOME=/home/app
cd /app

# --- operator runtime overrides (SSH-editable; no Coolify env UI needed) --------
# A KEY=value file on a persistent volume lets non-secret config be tuned by
# editing it over SSH + redeploying — instead of the Coolify env UI. Values here
# OVERRIDE the container env (last write wins). Intended for knobs like
# ROUTER_ALTERNATE, WINDOW_BUDGET_USD, CODEX_WINDOW_LIMIT, MODEL, CLAUDE_EFFORT,
# LOOP_INTERVAL. Secrets may go here too but are better left as Coolify secrets.
RUNTIME_ENV_FILE="${RUNTIME_ENV_FILE:-/app/logs/runtime.env}"
if [ -f "$RUNTIME_ENV_FILE" ]; then
    echo "[entrypoint] applying runtime overrides from $RUNTIME_ENV_FILE"
    # Parse KEY=value literally (NOT `. file`) so values with shell-special chars
    # — e.g. a Coolify token like `1|abcdef` whose `|` would otherwise be read as a
    # pipe — are exported verbatim. Handles `=` in the value and optional quotes.
    while IFS= read -r _line || [ -n "$_line" ]; do
        case "$_line" in ''|\#*) continue ;; esac
        _k=${_line%%=*}
        _v=${_line#*=}
        _k=$(printf '%s' "$_k" | tr -d '[:space:]')
        case "$_v" in
            \"*\") _v=${_v#\"}; _v=${_v%\"} ;;
            \'*\') _v=${_v#\'}; _v=${_v%\'} ;;
        esac
        [ -n "$_k" ] && export "$_k=$_v"
    done < "$RUNTIME_ENV_FILE"
    unset _line _k _v
fi

# --- required auth (from `claude setup-token`, injected as a Coolify secret) ---
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    echo "FATAL: CLAUDE_CODE_OAUTH_TOKEN is not set." >&2
    echo "Generate it with 'claude setup-token' and set it as a Coolify secret." >&2
    exit 1
fi

# --- runtime dirs (also mounted as persistent volumes) ---
mkdir -p memories projects logs

# --- persist docs/ across redeploys ---------------------------------------------
# Agents write deliverables to docs/<role>/ (per CLAUDE.md), but docs/ is NOT a
# mounted volume, so cycle docs (decision rationale, research, build logs) are
# wiped on every redeploy. Back docs/ with the persistent memories volume via a
# symlink. The image ships an (essentially empty, docs/* is gitignored) docs/ dir;
# migrate it into the store without clobbering persisted files, then symlink.
DOCS_STORE="${DOCS_STORE:-/app/memories/_docs}"
mkdir -p "$DOCS_STORE"
if [ ! -L /app/docs ]; then
    if [ -d /app/docs ]; then
        cp -a -n /app/docs/. "$DOCS_STORE/" 2>/dev/null || true
        rm -rf /app/docs
    fi
    ln -s "$DOCS_STORE" /app/docs
    echo "[entrypoint] docs/ -> $DOCS_STORE (persistent)"
fi

# --- persist .claude/skills/ so company-authored skills survive redeploys --------
# The company can author new skills via skill-creator, but .claude/skills/ ships in
# the image (not a volume) so they'd be wiped on redeploy. Back it with the memories
# volume: seed the image's base skills into the store without clobbering persisted
# ones, then symlink. The symlink must exist BEFORE the loop starts so Claude Code
# discovers the full set. (APP-204)
SKILLS_STORE="${SKILLS_STORE:-/app/memories/_skills}"
mkdir -p "$SKILLS_STORE"
if [ ! -L /app/.claude/skills ]; then
    if [ -d /app/.claude/skills ]; then
        # clobber (no -n): base skills stay repo-authoritative (image updates win),
        # while company-authored skills (unique names, not in the image) are left
        # untouched in the store and thus persist.
        cp -a /app/.claude/skills/. "$SKILLS_STORE/" 2>/dev/null || true
        rm -rf /app/.claude/skills
    fi
    ln -s "$SKILLS_STORE" /app/.claude/skills
    echo "[entrypoint] .claude/skills/ -> $SKILLS_STORE (persistent)"
fi

# --- the company's own git identity for its commits/deploys (optional) ---
[ -n "${COMPANY_GIT_NAME:-}" ]  && git config --global user.name  "$COMPANY_GIT_NAME"
[ -n "${COMPANY_GIT_EMAIL:-}" ] && git config --global user.email "$COMPANY_GIT_EMAIL"
git config --global --add safe.directory /app || true

# --- GitHub auth for the company's own pushes / repo creation ---
# gh CLI reads GH_TOKEN automatically; wire git push (HTTPS) to the same token.
if [ -n "${GH_TOKEN:-}" ]; then
    printf 'https://x-access-token:%s@github.com\n' "$GH_TOKEN" > "$HOME/.git-credentials"
    chmod 600 "$HOME/.git-credentials"
    git config --global credential.helper store
fi

# --- Codex fallback auth (optional) ---
# Codex (0.144.x) owns the ChatGPT OAuth session: during `codex exec` it refreshes
# and ROTATES the tokens, writing the new refresh/access tokens back to auth.json.
# So CODEX_HOME must live on a PERSISTENT volume and CODEX_AUTH_B64 must only SEED
# it on first boot — re-writing the original secret every restart resurrects an
# already-used refresh token and 401s ("refresh token was already used"). We put
# CODEX_HOME inside the persistent logs volume (no extra Coolify mount needed) and
# force the file credential store (no keyring in a container).
export CODEX_HOME="${CODEX_HOME:-/app/logs/.codex}"
mkdir -p "$CODEX_HOME" && chmod 700 "$CODEX_HOME"
if [ ! -f "$CODEX_HOME/config.toml" ]; then
    cat > "$CODEX_HOME/config.toml" <<'EOF'
model = "gpt-5.6-sol"
model_reasoning_effort = "low"
approval_policy = "never"
cli_auth_credentials_store = "file"
EOF
fi
if [ -s "$CODEX_HOME/auth.json" ]; then
    # Persisted (possibly rotated) auth already present — never overwrite it.
    chmod 600 "$CODEX_HOME/auth.json" 2>/dev/null || true
    export FALLBACK_ENGINE="${FALLBACK_ENGINE:-codex}"
    echo "[entrypoint] Codex auth: using persisted $CODEX_HOME/auth.json"
elif [ -n "${CODEX_AUTH_B64:-}" ]; then
    # First boot only: seed auth.json from the bootstrap secret.
    if echo "$CODEX_AUTH_B64" | base64 -d > "$CODEX_HOME/auth.json" 2>/dev/null; then
        chmod 600 "$CODEX_HOME/auth.json"
        export FALLBACK_ENGINE="${FALLBACK_ENGINE:-codex}"
        echo "[entrypoint] Codex auth: seeded from CODEX_AUTH_B64 (first boot)"
    else
        echo "[entrypoint] warning: CODEX_AUTH_B64 failed to decode; Codex disabled" >&2
    fi
else
    echo "[entrypoint] Codex auth: none present; Codex fallback disabled"
fi

DASHBOARD_PORT="${DASHBOARD_PORT:-8787}"

DASH_PID=""
LOOP_PID=""
term() {
    echo "[entrypoint] shutting down..."
    [ -n "$LOOP_PID" ] && kill -TERM "$LOOP_PID" 2>/dev/null || true
    [ -n "$DASH_PID" ] && kill -TERM "$DASH_PID" 2>/dev/null || true
}
trap term TERM INT

# --- dashboard (background), bound to all interfaces for Traefik/Cloudflare ---
echo "[entrypoint] starting dashboard on 0.0.0.0:${DASHBOARD_PORT}"
python3 dashboard/server.py --host 0.0.0.0 --port "$DASHBOARD_PORT" &
DASH_PID=$!

# --- autonomous loop (background so we can wait on both) ---
echo "[entrypoint] starting auto-loop (engine=${ENGINE:-claude})"
export ENGINE="${ENGINE:-claude}"
export CLAUDE_PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-bypassPermissions}"
./scripts/core/auto-loop.sh &
LOOP_PID=$!

# --- if either process exits, tear the container down so the runtime restarts it ---
wait -n "$DASH_PID" "$LOOP_PID"
echo "[entrypoint] a managed process exited; stopping container"
term
wait || true
exit 1
