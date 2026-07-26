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

echo "[heartbeat] starting — monitor=$MONITOR_SLUG interval=90s"
while true; do
    curl -s -m 10 -X POST "$CHECKIN_URL" \
        -H "Content-Type: application/json" \
        -d "{\"status\":\"ok\",\"monitor_config\":${MONITOR_CONFIG}}" \
        -o /dev/null || true
    sleep 90
done
