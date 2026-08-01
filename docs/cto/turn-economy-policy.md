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

## Guard rails in the machinery

- **Self-audit at an existing return moment** (never a new poll): after every jcode
  cycle, `scripts/ops/turn-audit.py --summary-last` classifies the session from
  jcode's own daily log and the loop logs a `[TURN-AUDIT …]` line. Verdicts:
  `CHATTY` (>60 turns), `BLOATED` (>120 messages ≈ 200K+ context). Non-ok verdicts
  are pushed to Telegram. Advisory — it never fails a cycle.
- **Cost floor vs booked cost.** The audit line's `floor_usd` prices cache traffic
  only (in/out tokens are redacted in jcode's log). A booked cycle cost many times
  the floor plus a `[COST] estimated (uncalibrated model)` line means the 5x
  unknown-model row fired (typical after a timeout kill), NOT that the cycle really
  burned that much. The ledger keeps the conservative figure by design — never
  "correct" it downward without an operator ruling.
- **Known gap (operator decision pending):** on a timeout kill the requested model
  IS known to the loop (the TIER line) even though the `done` event is gone. Passing
  it to the adapter as a hint would price timeout kills at ~1x instead of 5x. This
  loosens a REVISE-2 fail-closed invariant, so it is NOT implemented — recorded here
  for the APP-268 calibration review (due 2026-08-14).

## Diagnosis quick list (any agent, any harness)

- Tool round-trips more often than every 60s that aren't productive work? → rules 1-2.
- Wait/poll share of turns above 20%? → structural, fix the pattern.
- Long outputs flowing into context? → rule 2.
- No context-ceiling/compact rule? → rule 3.
- No self-audit or independent watchdog? → wire `turn-audit.py` at a return moment.
- Rules only in session memory instead of a document? → they die on restart; this
  file is the document.
