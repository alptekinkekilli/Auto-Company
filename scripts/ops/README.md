# Host-side operations scripts

These run on the **Docker host** (not inside the container), installed under
`/usr/local/bin/` and driven by root's crontab. They were previously untracked —
they existed only on the server, so they were unbacked and impossible for a fork
to reproduce. Keep this directory and the host in sync by hand when either changes.

| script | cron | what it does |
|---|---|---|
| `opportunity-analyst-cron.sh` | `30 4 * * *` | Runs the in-container Codex second-brain (APP-221). Waits up to 25 min for a codex-idle window so it does not collide with the loop's own Codex cycle, then execs `scripts/analyst/opportunity-analyst.sh` inside the app container. Logs to `/var/log/opportunity-analyst.log`. |
| `docker-prune-safe.sh` | `0 4 * * *` | Threshold-gated cleanup: build cache, unused images, **stopped containers**. Never touches volumes. |

## Two things to know before debugging with these

**`docker-prune-safe.sh` destroys crash evidence.** It runs `docker container prune -f`,
so a container that died overnight is gone by 04:00 along with its logs and exit
code. On 2026-07-24 a container stopped at 23:21 and was pruned at 04:00; by the
time anyone looked there was nothing left to inspect. If you are investigating a
crash, capture `docker logs` / `docker inspect` before the next 04:00.

**The analyst can "succeed" without producing anything.** `rc=0` alone is not proof
of a report — on 2026-07-25 a run exec'd into a container that was restarting,
emitted nothing, and logged a clean exit. The wrapper now requires `REPORT_OK` in
the output and exits `3` when it is missing, so the silent case is visible in
`/var/log/opportunity-analyst.log` as `FAILED ... no REPORT_OK`.
