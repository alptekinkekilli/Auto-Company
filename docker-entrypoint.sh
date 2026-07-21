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

# --- required auth (from `claude setup-token`, injected as a Coolify secret) ---
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    echo "FATAL: CLAUDE_CODE_OAUTH_TOKEN is not set." >&2
    echo "Generate it with 'claude setup-token' and set it as a Coolify secret." >&2
    exit 1
fi

# --- runtime dirs (also mounted as persistent volumes) ---
mkdir -p memories projects logs

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
