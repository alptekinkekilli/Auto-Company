#!/usr/bin/env bash
# APP-207: prevent redeploy churn from filling the 38GB disk.
# Threshold-gated: only prunes when disk >= THRESH%. SAFE — build cache + unused
# images + stopped containers ONLY. NEVER touches volumes (company memories/projects/logs).
set -uo pipefail
THRESH="${THRESH:-70}"
WARN="${WARN:-60}"
LOG=/var/log/docker-prune-safe.log
WARN_STATE=/var/lib/docker-prune-safe.warned
use() { df --output=pcent / | tail -1 | tr -dc '0-9'; }

# Telegram goes through the container's notifier. The credentials live in
# /app/logs/runtime.env, which the entrypoint exports into the LOOP's process tree
# only — a fresh `docker exec` does not inherit them, so read the two keys from the
# file inside the container (never dot-source it: other values contain '|').
# Logs the delivery result: an alert that silently does nothing is worse than none.
notify() {
  local c res
  c=$(docker ps --format '{{.Names}}' | grep '^z12a992' | head -1) || true
  if [ -z "$c" ]; then
    echo "$(date -Is) NOTIFY skipped: app container not running" >> "$LOG"
    return 0
  fi
  res=$(printf '%s' "$1" | docker exec -i -u app "$c" bash -c '
      T=$(grep -m1 "^TELEGRAM_BOT_TOKEN=" /app/logs/runtime.env 2>/dev/null | cut -d= -f2-)
      C=$(grep -m1 "^TELEGRAM_CHAT_ID=" /app/logs/runtime.env 2>/dev/null | cut -d= -f2-)
      if [ -z "$T" ] || [ -z "$C" ]; then echo "NO_CREDS"; exit 0; fi
      export TELEGRAM_BOT_TOKEN="$T" TELEGRAM_CHAT_ID="$C"
      bash /app/scripts/core/telegram-notify.sh && echo "SENT"
    ' 2>&1 | tail -1) || true
  echo "$(date -Is) NOTIFY result=${res:-ERROR}" >> "$LOG"
}

U="$(use)"
echo "$(date -Is) disk=${U}% thresh=${THRESH}% warn=${WARN}%" >> "$LOG"

# Early warning: tell the operator BEFORE the automatic cleanup kicks in, so a
# growth problem can be handled deliberately instead of by an emergency prune.
# Once per day — this job runs every 2h and we do not want an alert every run.
if [ "${U:-0}" -ge "$WARN" ] && [ "${U:-0}" -lt "$THRESH" ]; then
  today="$(date -u +%F)"
  if [ "$(cat "$WARN_STATE" 2>/dev/null || true)" != "$today" ]; then
    notify "⚠️ Disk ${U}% on $(hostname) — warning at ${WARN}%, automatic docker prune fires at ${THRESH}%.
docker: $(du -sh /var/lib/docker 2>/dev/null | cut -f1) · images: $(docker images -q | wc -l | tr -d ' ')
Acting now avoids an emergency cleanup (which also deletes stopped containers, i.e. crash evidence)."
    echo "$today" > "$WARN_STATE"
    echo "$(date -Is) WARN sent (disk ${U}%)" >> "$LOG"
  fi
fi

if [ "${U:-0}" -ge "$THRESH" ]; then
  echo "$(date -Is) PRUNE start (disk ${U}% >= ${THRESH}%)" >> "$LOG"
  docker builder prune -af --keep-storage=5GB >> "$LOG" 2>&1 || true
  docker image prune -af                      >> "$LOG" 2>&1 || true
  # until=24h keeps containers that died in the last day: stopped containers cost
  # almost nothing (the space is in images and build cache) but they carry the logs
  # and exit codes needed to debug a crash — exactly what an emergency prune during
  # an incident would otherwise destroy.
  docker container prune -f --filter until=24h >> "$LOG" 2>&1 || true
  A="$(use)"
  echo "$(date -Is) PRUNE done (disk now ${A}%)" >> "$LOG"
  notify "🧹 Disk was ${U}% (>= ${THRESH}%) on $(hostname) — ran the safe docker prune. Disk now ${A}%.
Volumes untouched. Containers stopped within the last 24h were kept for debugging."
fi
