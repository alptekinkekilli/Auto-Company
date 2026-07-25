#!/usr/bin/env bash
# Opportunity Analyst daily cron (APP-221) — runs the in-container two-pass Codex
# second-brain when the company loop is NOT mid-codex-cycle (avoids auth/quota collision).
set -uo pipefail
LOG=/var/log/opportunity-analyst.log
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }

C=$(docker ps --format '{{.Names}}' | grep '^z12a992' | head -1)
[ -n "$C" ] || { echo "$(ts) no container" >> "$LOG"; exit 0; }

# wait up to ~25 min for a codex-idle window (the loop cycles ~every 15 min)
idle=0
for _ in $(seq 1 25); do
  if [ "$(docker exec "$C" sh -lc 'ps -eo args | grep -c "[c]odex exec"' 2>/dev/null)" = "0" ]; then idle=1; break; fi
  sleep 60
done
[ "$idle" = "1" ] || { echo "$(ts) skip: no codex-idle window in 25m" >> "$LOG"; exit 0; }

echo "$(ts) start ($C)" >> "$LOG"
out=$(docker exec -u app "$C" bash /app/scripts/analyst/opportunity-analyst.sh 2>&1); rc=$?
printf '%s\n' "$out" >> "$LOG"
# A run can exit 0 and still deliver nothing (e.g. the container restarted through
# the exec window, as on 2026-07-25). Treat "no REPORT_OK" as a failure so the
# silent case is visible instead of looking like a clean run.
if printf '%s' "$out" | grep -q 'REPORT_OK' && ! printf '%s' "$out" | grep -q 'registry: skipped'; then
  echo "$(ts) done rc=$rc" >> "$LOG"
elif printf '%s' "$out" | grep -q 'registry: skipped'; then
  # Pass 1 wrote the directive but pass 2 returned nothing, so the registry was
  # never updated. Half a run — surface it rather than log it as clean.
  echo "$(ts) FAILED rc=$rc — pass-2 produced no output, registry NOT updated" >> "$LOG"
  rc=$((rc == 0 ? 4 : rc))
else
  echo "$(ts) FAILED rc=$rc — no REPORT_OK in output (analyst produced no report)" >> "$LOG"
  rc=$((rc == 0 ? 3 : rc))
fi
exit "$rc"
