#!/usr/bin/env bash
# APP-207: prevent redeploy churn from filling the 38GB disk.
# Threshold-gated: only prunes when disk >= THRESH%. SAFE — build cache + unused
# images + stopped containers ONLY. NEVER touches volumes (company memories/projects/logs).
set -uo pipefail
THRESH="${THRESH:-70}"
LOG=/var/log/docker-prune-safe.log
use() { df --output=pcent / | tail -1 | tr -dc '0-9'; }
U="$(use)"
echo "$(date -Is) disk=${U}% thresh=${THRESH}%" >> "$LOG"
if [ "${U:-0}" -ge "$THRESH" ]; then
  echo "$(date -Is) PRUNE start (disk ${U}% >= ${THRESH}%)" >> "$LOG"
  docker builder prune -af --keep-storage=5GB >> "$LOG" 2>&1 || true
  docker image prune -af                      >> "$LOG" 2>&1 || true
  docker container prune -f                   >> "$LOG" 2>&1 || true
  echo "$(date -Is) PRUNE done (disk now $(use)%)" >> "$LOG"
fi
