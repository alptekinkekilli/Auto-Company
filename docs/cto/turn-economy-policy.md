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

## Rules (enforced via Runtime Guardrails 6-7)

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
  `CHATTY` (>40 turns), `BLOATED` (>80 messages). Non-ok verdicts are pushed to
  Telegram. Advisory — it never fails a cycle.
  **Thresholds tightened 2026-08-01 (were 60/120).** A real 58-turn / 118-message /
  $5.81 cycle scored "ok" by sitting just under both bars — the audit called a 45%
  overrun of rule 3 clean. The bars are now anchored to the guardrail the company is
  actually given (~40 tool calls), not to the worst run observed. Re-scored against
  that day's eight sessions the new bars flag exactly one, so they discriminate rather
  than nag. Widening them is loosening a measurement, not a policy.
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
