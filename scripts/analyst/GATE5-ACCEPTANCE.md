# Gate 5 — Analyst jcode Acceptance Run (plan; run after gate 4)

Prereq: gate 4 done (`jcode login --provider openai` in the pilot container's
`$HOME/.jcode`, operator-approved headless flow).

## The run

One-shot pilot container, REAL inputs but COPIES — the acceptance run must not
touch prod memories:

```bash
C=<prod-container>
docker run -d --name jcode-analyst-accept --entrypoint sleep \
  -e JCODE_NO_TELEMETRY=1 -u app autocompany-jcode:pilot 7200
# copy live inputs in (memories/, docs/research/, framework) via docker cp from prod
# copy the operator-authorized ~/.jcode auth dir in
docker exec -u app jcode-analyst-accept bash /app/scripts/analyst/opportunity-analyst-jcode.sh
```

## Pass criteria (all must hold)

1. `REPORT_OK` printed; `analysis-directive.md` produced with the jcode header line.
2. Report substance: respects portfolio scope (no archived/non-tender candidate
   nominated), follows the skill's output order, names verdicts for the live axes.
   Judge against the LAST CODEX RUN's report (`memories/analysis-directive.md` in
   prod) — equivalence of structure and discipline, not of wording.
3. Pass-2: `merge_registry.py` reports a clean merge or a clean no-op — NOT
   "skipped". Every candidate ID preserved (the merger enforces it; verify its
   output line says so).
4. Pass-3 promotion gate runs and reports (promotion itself will almost certainly
   be BLOCKED on a copy — that is fine; it must not error).
5. `analyst-jcode-sessions.log` gained exactly the run's session ids.
6. Two `COST pass-*` lines in progress — `estimated:true` is acceptable until the
   gpt-5.6-sol price row is calibrated; `unavailable` is NOT.
7. No jcode processes left in the container afterwards; no writes outside
   analysis-directive.md / candidate-registry.md / analyst-progress.md +
   the two logs (diff the copied tree to prove it).
8. MODEL line check: progress header says `model=gpt-5.6-sol` AND the ndjson done
   event agrees — guards the silent-fallback trap end-to-end.
9. Tool discipline: the report must not claim it "could not read" the skill or
   inputs (read tool exposure), and must not have used bash to bypass a missing
   MCP (not applicable here — analyst needs no MCP — but grep the events for
   curl-to-API-endpoints as a sanity line).

## Price calibration (folds into this run)

From the acceptance ndjson: token totals × candidate gpt-5.6-sol list prices vs
`ccusage codex session` on a comparable codex run. Write the verified row into
`scripts/core/engine-usage-cost.py` PRICES and drop `estimated` for this model.

## After PASS

Operator decision to cut over: point `/usr/local/bin/opportunity-analyst-cron.sh`
at `opportunity-analyst-jcode.sh` (one line), keep the codex line commented for
rollback, 24h watch (gate 6). The cron's codex-idle wait-loop becomes vestigial
but harmless — remove it only after the LOOP's codex engine also migrates.
