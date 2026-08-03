---
name: prompt-optimization
description: Trigger-based maintenance of the loop's assembled prompt (PROMPT.md + runtime guardrails + consensus). Measure first, change structurally, prove with a held one-shot A/B. Use when PROMPT-SIZE fires repeatedly, bloat-trend regresses, a new prompt mechanism lands, or the engine/model changes.
---

# Prompt Optimization

The assembled cycle prompt is a cost surface (re-billed every tool turn) and a behavior
surface (rules the model actually follows vs. rules that just read well). This skill keeps
both honest. It is TRIGGER-based, not calendar-based.

## Triggers — run this skill when any of these is true

1. `[PROMPT-SIZE]` fired on ≥2 consecutive cycles (flip-flopping between prompt variants
   also invalidates cache from the switch point on).
2. `bloat-trend.py` reports a sustained regression window.
3. A new mechanism was added to the prompt (new guardrail, injected block, feedback line).
4. The engine or model changed.

## The five steps — in order, no skipping

**1. MEASURE (before touching anything).**
Section-level byte breakdown of PROMPT.md and consensus.md (script pattern: sizes per
`^#{1,3} ` heading). Last 24h of TURN-AUDIT lines (turns, floor_usd, verdict) — this is
your A/B baseline. PROMPT-SIZE firing history. Do not proceed on vibes; the 2026-08-03
audit found the real driver was turn count, not prompt size — measurement decided.

**2. RULE HYGIENE (enforceable-guardrails discipline).**
A rule earns its bytes only if it is mechanically checkable or demonstrably followed.
Hunt: rules restating other rules; rules about retired candidates/mechanisms; prose that
narrates instead of constrains. Bias one-in-one-out: a new rule should name what it
replaces. NEVER remove anything the guardrail-invariant sweep or directive-rule-sweep.py
checks for without updating those checks in the same commit — the loop refuses to boot on
a missing mandatory guardrail.

**3. STRUCTURE (the cache/attention compromise, from the platform docs).**
- STABLE PREFIX FIRST: PROMPT.md and static guardrails lead; anything volatile
  (feedback lines, snapshots, per-cycle state) goes as LATE as possible — a change
  invalidates cache from that point onward.
- INSTRUCTIONS AT THE END: long-context guidance puts data above and the operative ask
  at the bottom (up to ~30% quality effect). The tail block (`<cycle_orders>`) restates
  this cycle's priorities compactly AFTER the consensus data.
- XML TAGS over markdown headings for mixed instruction/context prompts
  (`<rules>`, `<state_snapshot>`, `<consensus>`, `<cycle_orders>`).
- Kill variant flip-flop: if a size guard switches prompt shapes near a threshold, fix
  the size, don't live on the boundary.

**4. VERIFY MECHANICALLY.**
`bash -n` on the assembly script, `tests/test_prompt_assembly.sh` (it evaluates the real
assignment blocks — it has caught a raw-quote kill twice), the guardrail-invariant sweep.
A prompt change that only "looks right" in the diff has not been verified.

**5. PROVE WITH A HELD ONE-SHOT A/B.**
Pre-register the metric BEFORE the run (e.g. "turns and floor_usd at-or-below the 24h
median for comparable work"). Then: arm LOOP_HOLD → sync → restart (held boot) → one-shot
token → compare TURN-AUDIT against the baseline from step 1. Regression = revert, not
rationalize. The 85→53-turn measurement on 2026-08-03 is the reference for what evidence
looks like.

## Standing cautions

- Consensus is the company's baton: compaction moves superseded blocks to an archive file
  with a pointer, during a WAIT window, with a backup — never silent deletion, and never
  touch the sections the current cycle's skeleton requires.
- Every applied change gets the out-of-band stamp in consensus (see
  out-of-band-merge-protocol) so cycles don't burn turns re-discovering it.
- This file is itself prompt surface for whoever loads it. Keep it under ~90 lines.
