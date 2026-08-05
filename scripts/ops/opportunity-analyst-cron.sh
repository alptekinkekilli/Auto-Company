#!/usr/bin/env bash
# Opportunity Analyst daily cron (APP-221) — jcode cutover 2026-07-31 (gate 6).
# ROLLBACK: ANALYST_ENGINE=codex reverts to the old in-container Codex path below,
# byte-identical to /usr/local/bin/opportunity-analyst-cron.sh.bak-codex-2026-07-31.
set -uo pipefail
LOG=/var/log/opportunity-analyst.log
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
ENGINE="${ANALYST_ENGINE:-jcode}"

C=$(docker ps --format "{{.Names}}" | grep "^z12a992" | head -1)
[ -n "$C" ] || { echo "$(ts) no container" >> "$LOG"; exit 0; }

# ---- Sentry Crons liveness (2026-08-04). Why: the 04:30 run died silently on a
# missing image tag (autocompany-jcode:pilot pruned in a deploy window) and nobody
# knew until the operator happened to ask. Check-in pattern mirrors
# scripts/core/sentry-heartbeat.sh: monitor_config inline (auto-creates), DSN read
# from the prod container's runtime.env so the host keeps no secret copy,
# best-effort — a failed check-in never affects the run. in_progress opens the
# window; a run that dies without a closing check-in trips max_runtime; a morning
# where cron never fires at all trips checkin_margin.
SLUG="opportunity-analyst-daily"
MON_CFG='{"schedule":{"type":"crontab","value":"30 4 * * *"},"checkin_margin":45,"max_runtime":90,"failure_issue_threshold":1,"recovery_threshold":1,"timezone":"UTC"}'
DSN=$(docker exec "$C" sed -n "s/^SENTRY_DSN=//p" /app/logs/runtime.env 2>/dev/null | head -1)
CHECKIN_URL=""
if [ -n "$DSN" ]; then
  _s="${DSN#*://}"; _k="${_s%%@*}"; _r="${_s#*@}"; _h="${_r%%/*}"; _p="${_r##*/}"
  if [ -n "$_k" ] && [ -n "$_h" ] && [ -n "$_p" ] && [ "$_k" != "$DSN" ]; then
    CHECKIN_URL="https://${_h}/api/${_p}/cron/${SLUG}/${_k}/"
  fi
fi
checkin() {
  [ -n "$CHECKIN_URL" ] || return 0
  curl -s -m 10 -X POST "$CHECKIN_URL" -H "Content-Type: application/json" \
    -d "{\"status\":\"$1\",\"monitor_config\":${MON_CFG}}" -o /dev/null || true
}
checkin in_progress

# codex-idle guard: kept for BOTH engines while the company loop still runs the
# codex CLI (vestigial for jcode auth, still avoids CPU/token contention).
idle=0
for _ in $(seq 1 25); do
  if [ "$(docker exec "$C" sh -lc "ps -eo args | grep -c \"[c]odex exec\"" 2>/dev/null)" = "0" ]; then idle=1; break; fi
  sleep 60
done
# a skipped day is a day the analyst did NOT run — that is a liveness failure,
# not a clean exit, even though the skip itself is deliberate.
[ "$idle" = "1" ] || { echo "$(ts) skip: no codex-idle window in 25m" >> "$LOG"; checkin error; exit 0; }

if [ "$ENGINE" = "codex" ]; then
  # ---- legacy path (rollback) ----
  echo "$(ts) start ($C) [engine=codex]" >> "$LOG"
  out=$(docker exec -u app "$C" bash /app/scripts/analyst/opportunity-analyst.sh 2>&1); rc=$?
else
  # ---- jcode path: one-shot pilot container, PROD volumes mounted so outputs
  # land in the real memories/logs; live docs/research copied in each run
  # (docs is container-layer state in prod, not a volume). ----
  echo "$(ts) start ($C) [engine=jcode one-shot]" >> "$LOG"
  RUN=analyst-jcode-run
  docker rm -f "$RUN" >/dev/null 2>&1 || true
  # Image resolution (2026-08-05). Why: this hardcoded `autocompany-jcode:pilot`, and
  # that tag has now been deleted THREE times by /etc/cron.d/docker-prune-safe — its
  # WARN branch runs `docker image prune -af` every 2h once disk >= 60%, and the keeper
  # containers anchor 378d6a3 and r2, not `pilot`. Retagging fixes the morning and
  # nothing else, so stop depending on one tag: prefer pilot, else fall back to whatever
  # autocompany-jcode image the keepers are holding (newest first). A missing image is
  # now FATAL rather than a silent `docker run` failure followed by a cascade of
  # "No such container" execs and a report-less run.
  IMG=autocompany-jcode:pilot
  if ! docker image inspect "$IMG" >/dev/null 2>&1; then
    ALT=$(docker images --format '{{.Repository}}:{{.Tag}}' autocompany-jcode 2>/dev/null | grep -v '<none>' | head -1)
    if [ -z "$ALT" ]; then
      echo "$(ts) FAILED — no autocompany-jcode image on host (pilot pruned, no fallback) [engine=jcode]" >> "$LOG"
      checkin error; exit 5
    fi
    echo "$(ts) WARN: $IMG missing (pruned?) — falling back to $ALT [engine=jcode]" >> "$LOG"
    IMG="$ALT"
  fi
  if ! docker run -d --name "$RUN" --entrypoint sleep \
    -v z12a992i3ty202zezspij2fn-ac-memories:/app/memories \
    -v z12a992i3ty202zezspij2fn-ac-logs:/app/logs \
    -v jcode-pilot-home:/home/app/.jcode \
    -e JCODE_NO_TELEMETRY=1 -u app "$IMG" 7200 >/dev/null 2>>"$LOG"; then
    echo "$(ts) FAILED — could not start one-shot container from $IMG [engine=jcode]" >> "$LOG"
    checkin error; exit 6
  fi
  # /app/docs in PROD is a symlink into the memories volume (/app/memories/_docs),
  # which this container already mounts — no copy needed, just mirror the symlink
  # over the image-baked stale docs dir. Discovered after two tar attempts failed.
  docker exec -u root "$RUN" sh -c "rm -rf /app/docs && ln -sfn /app/memories/_docs /app/docs"
  docker exec -u root "$RUN" chown -R app:app /app/docs /home/app/.jcode
  # scripts-refresh (2026-08-03): the pilot image bakes /app/scripts at build time,
  # so analyst-script changes deployed to PROD never reached this one-shot. Copy the
  # live prod tree over the baked one each run — prod (git-deployed) is the source
  # of truth; the image copy is only a fallback if this cp fails (logged, non-fatal).
  ST=$(mktemp -d)
  if docker cp "$C":/app/scripts "$ST/scripts" >/dev/null 2>&1 \
     && docker cp "$ST/scripts" "$RUN":/app/ >/dev/null 2>&1; then
    docker exec -u root "$RUN" chown -R app:app /app/scripts
    # tests-refresh (2026-08-03): the analyst re-runs the standing suites as directive
    # evidence; without the live tests its report judged them nonexistent (FINDING A).
    if docker cp "$C":/app/tests "$ST/tests" >/dev/null 2>&1 \
       && docker cp "$ST/tests" "$RUN":/app/ >/dev/null 2>&1; then
      docker exec -u root "$RUN" chown -R app:app /app/tests
    else
      echo "$(ts) WARN: tests refresh failed — analyst sees image-baked tests" >> "$LOG"
    fi
    docker cp "$C":/app/PROJECT_EVALUATION_FRAMEWORK.md "$ST/PEF.md" >/dev/null 2>&1 \
      && docker cp "$ST/PEF.md" "$RUN":/app/PROJECT_EVALUATION_FRAMEWORK.md >/dev/null 2>&1 \
      && docker exec -u root "$RUN" chown app:app /app/PROJECT_EVALUATION_FRAMEWORK.md
    echo "$(ts) scripts refreshed from $C" >> "$LOG"
  else
    echo "$(ts) WARN: scripts refresh from $C failed — running with image-baked copy" >> "$LOG"
  fi
  rm -rf "$ST"
  out=$(docker exec -u app "$RUN" bash /app/scripts/analyst/opportunity-analyst-jcode.sh 2>&1); rc=$?
  peak=$(docker exec "$RUN" cat /sys/fs/cgroup/memory.peak 2>/dev/null)
  case "$peak" in ("" | *[!0-9]*) peak="?" ;; (*) peak=$((peak/1048576)) ;; esac
  echo "$(ts) peak_mem=${peak}MB [engine=jcode]" >> "$LOG"
  docker rm -f "$RUN" >/dev/null 2>&1 || true
fi

printf "%s\n" "$out" >> "$LOG"
if printf "%s" "$out" | grep -q "REPORT_OK" && ! printf "%s" "$out" | grep -q "registry: skipped"; then
  echo "$(ts) done rc=$rc [engine=$ENGINE]" >> "$LOG"
elif printf "%s" "$out" | grep -q "registry: skipped"; then
  echo "$(ts) FAILED rc=$rc — pass-2 produced no output, registry NOT updated [engine=$ENGINE]" >> "$LOG"
  rc=$((rc == 0 ? 4 : rc))
else
  echo "$(ts) FAILED rc=$rc — no REPORT_OK in output (analyst produced no report) [engine=$ENGINE]" >> "$LOG"
  rc=$((rc == 0 ? 3 : rc))
fi
if [ "$rc" = "0" ]; then checkin ok; else checkin error; fi
exit "$rc"
