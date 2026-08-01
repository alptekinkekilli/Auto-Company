---
name: enforceable-guardrails
description: "Write agent rules that actually change behaviour instead of rules that read well and get ignored. Use when adding or revising a Runtime Guardrail, a PROMPT.md rule, a skill instruction, or any 'the company must stop doing X' policy — and whenever a rule you already shipped is being violated. Ranks enforcement mechanisms from mechanical to advisory and requires the cheapest mechanical option available before prose."
argument-hint: "[the behaviour you want to change]"
---

# Enforceable guardrails — why one rule landed and the other didn't

Two guardrails shipped to the same loop, into the same prompt, on the same day. One changed
behaviour on its first cycle. The other has never been obeyed. The difference is not
emphasis, and it is not the model.

| | Guardrail 7 (TURN ECONOMY) | Guardrail 8 (NARROW READS) |
|---|---|---|
| what it says | "after roughly 40 tool calls, STOP investigating" | "use `--formula` / `--fields` / `--max-records`" |
| asks for | restraint | a parameter |
| first cycle carrying it | **78 turns / 156 messages, BLOATED** | Airtable reads **3.2 KB avg** vs 28.7 KB before |
| enforcement available | none (jcode has no max-turns flag) | tool deny + a wrapper that refuses |

A rule that asks an agent to want less is a wish. A rule that names the flag to type is an
instruction. And a rule the machinery makes impossible to break needs no compliance at all.

## The ladder — always take the lowest rung that exists

Work DOWN this list and stop at the first rung you can actually build. Shipping prose when
rung 1 or 2 was available is the mistake this skill exists to prevent.

1. **Make it impossible.** Remove the capability: deny the tool, drop the permission, delete
   the code path. `mcp__airtable__list_records_for_table` in `JCODE_TOOLS_DENY` is not a rule
   about whole-table reads; it is the end of whole-table reads on that path.
2. **Make it refuse, with the remedy in the refusal.** A wrapper that fails closed and prints
   the exact flag that fixes it (`scripts/ops/airtable-read.py`). A refusal without a remedy
   is just an obstacle, and obstacles get routed around — usually by something worse.
3. **Name the parameter, not the virtue.** If it must be text, make it copy-pasteable:
   the flag, the function, the file path, the threshold as a number. "Be economical" is
   unactionable; "`--max-records 20`" is one keystroke.
4. **Attach the measurement to the rule.** Numbers survive re-reading; adjectives don't.
   "$2.38 vs $0.34 over 7 cycles" is why the rule exists, and it is what stops a future
   session from quietly relaxing it.
5. **Advisory prose alone.** Nearly worthless as enforcement. Legitimate only for judgement
   calls that genuinely cannot be mechanised — and then say so, so nobody mistakes it for
   a control.
6. **After-the-fact audit.** `[TURN-AUDIT … verdict=BLOATED]` is a feedback signal, not a
   guardrail. Never report an audit line as if it were enforcement.

## Before you write the rule

- **Measure the thing first.** You cannot tell whether a rule worked without a before number
  on the same window. See the `cost-measurement` skill for how not to fool yourself here.
- **Find the real actor.** The measured Airtable cost was the company's own bookkeeping, not
  the "expensive" web research everyone assumed. A rule aimed at the wrong actor is worse
  than none: it looks like the problem is handled.
- **Check the tool's own API first** (Context7 for anything external). `filterByFormula`,
  `fields[]`, `maxRecords`, the 16,000-character URL limit and the POST fallback are all
  documented behaviours — the rule is only writable because the parameters exist.
- **Ask what breaks if it's obeyed.** Denying a tool removes a capability; make sure the
  replacement path exists and is live-tested BEFORE the deny ships, not after.

## Writing it

- Put it where it is read every time, not where it is read once. In this repo that is
  `## Runtime Guardrails` in `scripts/core/auto-loop.sh` — **and there are TWO prompt-assembly
  branches** (normal and read-by-reference). A rule added to one branch silently vanishes on
  large-prompt cycles. `grep -c` for your rule; the answer must be 2.
- Durable rationale goes in `docs/cto/` and is referenced by the rule. Note that
  `/app/docs/` and `/app/memories/_docs/` are the SAME inode in production: a deploy does not
  update them, only a write into the volume does.
- Keep the rule one paragraph. It competes for attention with every other rule on every turn.
- A skill's frontmatter `description` is what decides whether it gets loaded at all — write it
  as "use when …", naming the situations, not the topic. A skill can also inject live context
  with `` !`command` ``, which turns a static instruction into a current one.

## Verifying it landed

1. **Deployed script, not the stream.** Cycle ndjson does NOT record the prompt: grep for your
   rule there and you get 0 — so does `TURN ECONOMY`, which has shipped for days. Verify in the
   file that actually ran (`docker exec … grep -c 'YOUR RULE' /app/scripts/core/auto-loop.sh`).
2. **Behaviour on the next cycle, scored alone.** Aggregate reports mix pre- and post-change
   cycles and will tell you nothing changed. Score the new cycle by itself.
3. **Report the ceiling honestly.** One cycle is a signal, not proof. Say which it is.
4. **If it was ignored, do not rewrite it louder.** Go one rung DOWN the ladder.
