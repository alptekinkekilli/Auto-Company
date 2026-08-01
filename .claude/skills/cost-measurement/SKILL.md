---
name: cost-measurement
description: "Measure what a cycle actually costs before changing anything about it. Use when spend looks wrong, when asked where the tokens go, when checking whether an efficiency change worked, or before proposing any optimisation. Covers the residual-cost model (size x turns remaining), the existing measurement scripts, and the five traps that have already produced wrong answers in this system."
argument-hint: "[what you are trying to find out]"
---

# Cost measurement — get the number before you get an opinion

Every efficiency decision in this system that was made from intuition was wrong. Web research
"felt" expensive and was 4% of the bill. A $73.94 window "was" runaway spend and was 86%
accounting artefact. The company's own bookkeeping reads — the boring part nobody suspected —
were the largest single context cost in the system. Measure first; the intuition is not a
prior worth having.

## The model everything else follows

**A tool result is not paid once.** It enters the context and is re-read on every later turn
of that cycle. So:

```
cost of a call ≈ output_tokens × turns REMAINING after it × cache-read rate
```

Consequences that keep mattering:
- **Size and timing multiply.** 170,958 bytes at turn 7 of a 74-turn cycle → re-read 67 times
  → ~$0.98 for one call. The identical bytes at turn 60 → ~$0.10.
- **Every tool call is also a turn**: the whole conversation is re-sent to decide the next
  step. Ten tiny fetches cost ten context re-reads regardless of payload.
- **Therefore the two levers are payload size and how early it lands** — not "fewer, bigger
  calls" or "more, smaller calls" as a slogan.

## The instruments (use them; do not re-derive)

| script | question it answers |
|---|---|
| `scripts/ops/web-research-cost.py` | which TOOLS put bytes in context, and what the re-reads cost |
| `scripts/ops/turn-audit.py` | how chatty a session was (turns, messages, verdict) |
| `scripts/ops/cost-audit.py` | the deterministic daily cost report → `memories/cost-audit.md` |
| `scripts/core/engine-usage-cost.py` | per-cycle pricing from the stream, including killed cycles |

Interpret their output. Do not recompute their numbers by hand in a report — divergent
arithmetic between two places is how a wrong number gets a second life.

## The five traps (each one has already produced a wrong answer here)

1. **The window you measured is not the window you were asked about.** An aggregate over the
   last 7 cycles, 6 of them from before the change, reported "28.7 KB average — no effect"
   while the one cycle after the change was 3.2 KB. Score the cycle or day in question BY
   ITSELF, then compare.
2. **Pre-filtering by category answers the question you assumed.** The first version of
   `web-research-cost.py` scored only web tools and reported $0.34 as if it were the total —
   true, and misleading, because it excluded the biggest source in the data. Score everything,
   then rank.
3. **The prompt is not in the cycle ndjson.** `grep "NARROW READS" cycle-*.ndjson` returns 0 —
   so does `grep "TURN ECONOMY"`, which has been in every prompt for days. Absence there is
   not evidence. Verify prompt content in the deployed script.
4. **Killed cycles lie about cost.** A watchdog-killed cycle loses its `done` event; without a
   model name the adapter prices at the unknown-model row × 5.0. One such cycle booked $63.63
   against a real ~$12.7 and filled 64% of the 5h window — which then SUPPRESSED the effort
   ladder, making per-cycle cost look like it had improved. Before reading any window, check
   for `estimated:true` rows. A cost improvement with a phantom in the window is not an
   improvement.
5. **There is no cross-check under jcode.** ccusage returns EMPTY for Claude (jcode writes no
   claude-CLI JSONL), so the 5h window is 100% ledger-derived. A mispriced row has nothing to
   correct it. Treat ledger numbers as the only source and audit them accordingly.

## Procedure

1. **State the question in one sentence**, including the window ("what did cycle #1 on
   2026-08-01 spend on Airtable reads?"). Vague questions produce aggregate answers.
2. **Pick the window deliberately** and say so in the output. Never let the tool's default
   window silently become the answer's scope.
3. **Rank by cost, not by call count.** 149 bash calls at 1.2 KB each matter less than 30
   Airtable calls at 28.7 KB.
4. **Separate transfer from context.** Bytes fetched and discarded (a `--count-only`) are
   nearly free; bytes that land in the conversation are re-billed for the rest of the cycle.
5. **Report the delta with its ceiling.** "3.2 KB vs 28.7 KB on one cycle — a signal, not
   proof" is a complete finding. A number without its window is not.
6. **State the notional/real distinction.** These dollars are API-equivalent on a Max
   subscription, not billed cash. Their real job is driving the four budget gates — which is
   exactly why a phantom row matters: it can trip a gate no real usage justified.

Durable policy: `docs/cto/turn-economy-policy.md`. To turn a finding into a rule that actually
holds, use the `enforceable-guardrails` skill — a measurement that ends in advisory prose
usually ends in nothing.
