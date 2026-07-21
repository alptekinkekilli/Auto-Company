#!/usr/bin/env bash
# Dry-run the cost-alerting cron handler against a local wrangler dev server.
#
# Prereqs:
#   1. `npm run db:local` — apply migrations to local D1.
#   2. `npx wrangler dev --port 8891 --local --test-scheduled` — start dev server.
#      (--test-scheduled is what makes the /__scheduled endpoint available.)
#
# Then run this script. It will:
#   - Seed enough events into usage_events to trip the 14-day cache-hit-rate
#     alert (needs >=500 events with hit rate < 70%).
#   - POST to /__scheduled to fire the cron handler.
#   - Confirm the alert appears in wrangler dev's stdout log lines.
#
# Cleanup: this seeds throwaway rows into the local Miniflare DB. Reset with
# `rm -rf .wrangler/state/v3/d1` if you want a clean slate.

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8891}"

echo "==> health check"
curl -sf "${BASE_URL}/health" >/dev/null || { echo "wrangler dev not up on ${BASE_URL}"; exit 1; }
echo "OK"

echo "==> pick or create an API key to attribute seeded events to"
KEY_ID="$(npx wrangler d1 execute snapog-db --local --json \
  --command "SELECT id FROM api_keys ORDER BY created_at DESC LIMIT 1" \
  2>/dev/null | grep -o '"id": *"[^"]*"' | head -1 | cut -d'"' -f4 || true)"

if [[ -z "${KEY_ID}" ]]; then
  echo "no api keys yet — register one via POST /register first"
  exit 1
fi
echo "using api_key_id=${KEY_ID}"

echo "==> seed 500 cache-miss events in the last 24h"
npx wrangler d1 execute snapog-db --local --command "
INSERT INTO usage_events (id, api_key_id, template, cache_hit, generated_at)
SELECT
  lower(hex(randomblob(16))),
  '${KEY_ID}',
  'default',
  0,
  datetime('now', printf('-%d minutes', abs(random()) % 1440))
FROM (
  WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt WHERE x<500)
  SELECT x FROM cnt
);
" >/dev/null

echo "==> fire the cron handler"
curl -s "${BASE_URL}/__scheduled?cron=0+*/6+*+*+*"
echo
echo
echo "==> expected in wrangler dev logs:"
echo "  [alerts] ALERT_WEBHOOK_URL unset; alerts would have fired: [...cache_hit_rate...]"
echo "  [cron] cost-alert check fired 1 alert(s)"
echo
echo "If ALERT_WEBHOOK_URL is set as a secret, a POST goes there instead."
