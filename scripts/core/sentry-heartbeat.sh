#!/usr/bin/env bash
# Background heartbeat for Sentry Crons — proves the CONTAINER itself is alive,
# independent of loop cycle duration or dashboard request handling.
#
# Why this exists (APP-250): the container crash-looped twice (2026-07-24 and
# 2026-07-26) and both times nobody found out until hours later, by which point
# Docker's restart-manager had already given up and removed the container along
# with its logs. Application-level error reporting (dashboard/sentry_client.py)
# can't see this failure mode — it only runs INSIDE the process that's dying.
# This script runs as its own background process, checking in to a Sentry Crons
# monitor every 90s. If the whole container (PID 1) goes down, this process dies
# with it and check-ins stop — Sentry flags the monitor "missed" within minutes,
# not hours, and (once an alert rule is wired to it, see docs/devops/) that can
# page out via a Cloudflare Worker webhook relay to Telegram in near-real-time.
#
# Best-effort only: a failed check-in must never affect the dashboard or loop.
set -uo pipefail

DSN="${SENTRY_DSN:-}"
if [ -z "$DSN" ]; then
    echo "[heartbeat] SENTRY_DSN not set — heartbeat disabled"
    exit 0
fi

# Parse the DSN ourselves (same approach as dashboard/sentry_client.py) — no
# pip deps, no sentry-sdk. Format: https://<public_key>@<host>/<project_id>
_stripped="${DSN#*://}"
PUBLIC_KEY="${_stripped%%@*}"
_rest="${_stripped#*@}"
HOST="${_rest%%/*}"
PROJECT_ID="${_rest##*/}"

if [ -z "$PUBLIC_KEY" ] || [ -z "$HOST" ] || [ -z "$PROJECT_ID" ] || [ "$PUBLIC_KEY" = "$DSN" ]; then
    echo "[heartbeat] could not parse SENTRY_DSN — heartbeat disabled"
    exit 0
fi

MONITOR_SLUG="auto-company-container-heartbeat"
CHECKIN_URL="https://${HOST}/api/${PROJECT_ID}/cron/${MONITOR_SLUG}/${PUBLIC_KEY}/"

# schedule/checkin_margin are in minutes: expect a check-in every 2min, allow
# 2min of slack before Sentry calls it "missed" — so a dead container is
# flagged within ~4 minutes, not the ~2.5 hours it took last time.
MONITOR_CONFIG='{"schedule":{"type":"interval","value":2,"unit":"minute"},"checkin_margin":2,"max_runtime":1,"failure_issue_threshold":1,"recovery_threshold":1,"timezone":"UTC"}'

APP="${APP_DIR:-/app}"
DASHBOARD_PORT="${DASHBOARD_PORT:-8787}"
LOOP_PID_FILE="$APP/.auto-loop.pid"

# APP-250 follow-up (2026-07-27): this script is started BEFORE, and lives
# independently of, the dashboard/loop (see docker-entrypoint.sh's comment —
# its own death must never tear the container down). That means an unconditional
# "ok" every 90s only proves the CONTAINER PROCESS TREE exists, not that the
# company is doing anything — a restart storm that completes each crash/restart
# cycle in well under 4 minutes (the documented APP-240 stale-PID storm cycled
# every 5-10 min, which this WOULD have caught, but a faster one wouldn't) could
# keep producing "ok" check-ins forever while dashboard/loop never survive their
# first few seconds. Check both are actually alive before reporting "ok"; report
# "error" (Sentry treats this as an immediate failure, no need to wait out the
# missed-checkin margin) otherwise.
company_is_alive() {
    curl -s -m 5 -o /dev/null "http://127.0.0.1:${DASHBOARD_PORT}/api/status" || return 1
    [ -f "$LOOP_PID_FILE" ] || return 1
    kill -0 "$(cat "$LOOP_PID_FILE" 2>/dev/null)" 2>/dev/null || return 1
    return 0
}

echo "[heartbeat] starting — monitor=$MONITOR_SLUG interval=90s"
# Grace window: dashboard/loop are started via `&` at nearly the same moment as
# this script, but need a few seconds to bind their port / write their PID file.
# Checking immediately would false-positive "error" on every ordinary boot.
sleep 8
while true; do
    if company_is_alive; then
        status="ok"
    else
        status="error"
        echo "[heartbeat] dashboard/loop liveness check failed — reporting error"
    fi
    curl -s -m 10 -X POST "$CHECKIN_URL" \
        -H "Content-Type: application/json" \
        -d "{\"status\":\"${status}\",\"monitor_config\":${MONITOR_CONFIG}}" \
        -o /dev/null || true
    sleep 90
done
