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

**`docker-prune-safe.sh` would destroy crash evidence — but only above its threshold.**
It runs `docker container prune -f`, which deletes stopped containers along with
their logs and exit codes. It is gated at `THRESH=70%` disk, and the disk has been
sitting at 32-46%, so **it has not actually fired**. An earlier version of this
README claimed it pruned the container that died on 2026-07-24 — that was wrong:
the 04:00 run that day logged `disk=32% thresh=70%` and pruned nothing. What
removed that container is still unidentified (Coolify's own redeploy cleanup is
the likeliest candidate, unverified). Corrected here so nobody debugs from it.

Still worth knowing: if the disk ever does cross 70% during an incident, the
cleanup will take the evidence with it. Adding `--filter until=24h` to the
container prune would keep recent corpses at no meaningful disk cost — stopped
containers are tiny; the space lives in images and build cache.

**The analyst can "succeed" without producing anything.** `rc=0` alone is not proof
of a report — on 2026-07-25 a run exec'd into a container that was restarting,
emitted nothing, and logged a clean exit. The wrapper now requires `REPORT_OK` in
the output and exits `3` when it is missing, so the silent case is visible in
`/var/log/opportunity-analyst.log` as `FAILED ... no REPORT_OK`.

`REPORT_OK` alone is also not enough: the run has **two** passes, and pass 2 (the
registry update) can come back empty while pass 1 still reports success — the
tail then reads `registry: skipped (pass-2 no output)`. That happened on the
2026-07-25 manual run. The wrapper treats a skipped registry as a failure too
(exit `4`), because a directive without a registry update is half a run.

Suspected cause of that skip, unconfirmed: pass 2 feeds the whole report plus the
whole `candidate-registry.md` to Codex and asks for the **complete** rewritten
registry back as one JSON string. The registry has grown to ~119 KB, so the
required output alone is near or past the model's limit. If this recurs, the fix
is to ask for a patch/diff of the changed buckets rather than a full-file rewrite.
