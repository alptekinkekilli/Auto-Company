# Turn Economy Policy — why waiting and re-reading burn the budget

> Location note: at runtime `/app/docs` is a symlink into the persistent memories
> volume (`/app/memories/_docs`), which SHADOWS the image's copy of this file. The
> volume copy is what cycles read; this repo copy is version-controlled provenance.
> Update BOTH when the policy changes.

Adopted 2026-08-01 from the operator's cross-project guide (source case: the Wowcar
codex governor, where 55% of a day's spend went to wait turns). This document is the
durable home of the rules — the Runtime Guardrails injected into every cycle prompt
reference it, so the discipline survives restarts and compactions.

## The mechanism

The cost unit of an LLM agent is the **turn**, not wall-clock time. Every time the
model sees a tool result, the ENTIRE conversation context is re-billed as input
(cache discounts soften, never remove, this) and the model emits invisible reasoning
tokens at the output tariff. Therefore:

- `sleep 30` **inside the shell** → free (the CPU waits, the model does not run).
- returning to the model after each short sleep → one full turn each time.
- an agent polling every 30s burns ~120 empty turns/hour.

On the jcode-claude path there is a second multiplier measured in production
(2026-08-01, container `…-045249014236`): each turn re-writes ~130K tokens of
1h-cache at the 2x cache-write tariff, and once the conversation crosses ~200K
tokens the provider's long-context premium applies on top. Cycle #2 that day reached
**73 turns / 146 messages / 15.5M cache-read tokens**, timed out at 900s, lost its
tail work, and (because the timeout kill destroyed the `done` event) was booked at
the deliberate 5x conservative unknown-model estimate: $63.63 against a real burn of
roughly $12.7.

## Rules (enforced via Runtime Guardrails 6-8)

1. **Move waiting into the shell.** One blocking `until <cond>; do sleep 20; done`
   is ONE turn regardless of duration. Never sleep-and-recheck across tool calls.
2. **Output hygiene.** Long command output goes to a file (`> /tmp/out.log 2>&1`);
   the context gets only `tail -20` or a grep excerpt. Large memory files
   (`candidate-registry.md` 330KB, `decision-ledger.md` 221KB) are grep/offset-read,
   never dumped whole.
3. **Context ceiling.** After ~40 tool calls in a cycle, stop investigating: persist
   findings + Next Action to `memories/consensus.md` and END the cycle. The next
   cycle continues fresh — cheaper than a bloated context, and it cannot time out.
4. **Batch.** Related lookups go into one tool call where the tool allows (Airtable
   filterByFormula over per-record gets; one grep over repeated reads).
5. **Narrow reads — never pull a whole table.** Scope every collection read:
   `filterByFormula` (rows) + `fields[]` (columns) + `maxRecords` (ceiling). Measured
   2026-08-01 over 7 cycles: `mcp__airtable__list_records_for_table` averaged **29.5 KB
   per call** and its re-reads cost **$2.38** — 7x all external web research in the same
   window ($0.34, 78 calls). The five Qualified rows the company actually needed are
   **1.2 KB** when asked for by name. Applies to any tool that can return a whole
   collection, not only Airtable.
6. **Fetch late, not early.** Cost = output size x turns REMAINING. Worst call observed:
   170,958 bytes at turn 7 of a 74-turn cycle → re-read 67 times → ~$0.98 for one call.
   The same bytes at turn 60 would have cost ~$0.10. If a big read can wait until after
   the decisions that depend on the small ones, let it wait.

**Rule 3 is not self-enforcing.** jcode has no max-turns flag (checked 2026-08-01:
`--tools`, `--disabled-tools`, `--tool-profile` exist; no iteration cap), so the only
mechanical ceiling is `CYCLE_TIMEOUT_SECONDS` — and hitting it costs the cycle's tail
work. Text asking the company to stop at ~40 calls was measurably exceeded (58) on the
first cycle that carried it. Treat the audit's CHATTY/BLOATED line as the feedback
signal, not as proof the rule is being followed.

## Guard rails in the machinery

- **Self-audit at an existing return moment** (never a new poll): after every jcode
  cycle, `scripts/ops/turn-audit.py --summary-last` classifies the session from
  jcode's own daily log and the loop logs a `[TURN-AUDIT …]` line. Verdicts:
  `CHATTY` (>55 turns), `BLOATED` (>65 turns, OR >=675s, OR >=$5.00 floor). Only
  **BLOATED** is pushed to Telegram; CHATTY stays in the log. Advisory — never fails a cycle.
  **Recalibrated 2026-08-02 against 34 measured cycles**, replacing the 2026-08-01 bars
  (40 turns / 80 messages) which fired on **14 of 34 cycles — 41%**. An alarm at that rate
  is not a signal: it trains the reader to scroll past, and then the cycle that matters
  arrives looking exactly like the noise. Two defects showed up only once the distribution
  was plotted:
  * the bars sat inside normal behaviour — turns p50=34 / p75=49 / p90=65, msgs p50=69 /
    p75=102 / p90=130, so an 80-message bar is *below* the 75th percentile;
  * `msgs_max` was never independent — it is ~2x turns in every cycle (40/81, 46/92,
    78/156), so two thresholds voted twice on one fact and doubled the false alarms.
  What separates the harmful cycles is RISK, not chattiness: the tail runs 601-893s against
  the 900s watchdog (one was killed by it and lost its tail work) and costs $3.2-6.9. The
  bars now encode that directly, and `msgs_max` is reported but no longer votes.
  **Note the divergence with rule 3's "~40 tool calls":** the measured median cycle is 34
  turns and healthy cycles reach ~50. A feedback signal calibrated to a number reality never
  respects is worthless — fix the prose or fix the reality, but do not blunt the instrument.
  Widening these is loosening a measurement, not a policy: change them only with new
  distribution evidence, and state what the distribution was.
- **Cost floor vs booked cost.** The audit line's `floor_usd` prices cache traffic
  only (in/out tokens are redacted in jcode's log). A booked cycle cost many times
  the floor plus a `[COST] estimated (uncalibrated model)` line means the 5x
  unknown-model row fired (typical after a timeout kill), NOT that the cycle really
  burned that much. The ledger keeps the conservative figure by design — never
  "correct" it downward without an operator ruling.
- **Killed-cycle pricing — CLOSED 2026-08-01** (was "operator decision pending"). A
  timeout kill destroys the `done` event, so the adapter had no model name and priced
  at the unknown row x5: one cycle booked $63.63 against a real ~$12.7 and filled 64%
  of the 5h window alone, holding the effort ladder down for hours. The loop now passes
  `--model-hint`, consulted ONLY when there is no `done` event. What did NOT change:
  `done.model` still wins wherever it exists (the substitution guard is untouched), an
  unrecognised hint still falls through to the conservative row, and hinted results stay
  `estimated: true` with the hint named in `basis`. `tests/test_cost_model_hint.sh`.

## Diagnosis quick list (any agent, any harness)

- Tool round-trips more often than every 60s that aren't productive work? → rules 1-2.
- Wait/poll share of turns above 20%? → structural, fix the pattern.
- Long outputs flowing into context? → rule 2.
- No context-ceiling/compact rule? → rule 3.
- No self-audit or independent watchdog? → wire `turn-audit.py` at a return moment.
- Rules only in session memory instead of a document? → they die on restart; this
  file is the document.
