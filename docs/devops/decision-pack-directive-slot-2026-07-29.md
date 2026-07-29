# Adjudication brief — the single-slot directive channel (2026-07-29)

Auto-Company policy: judgement calls go to an independent high-capability model with an evidence
pack. The assembler builds the pack and does not rule.

**You are the adjudicator. You have not seen the conversation that produced this. Verify against
the files before ruling — the pack may overstate.** This pack is deliberately in `docs/devops/`
rather than `memories/`, because `memories/*` is gitignored (`.gitignore:193-195`) and a previous
pack cited line numbers in files no adjudicator could reach. Everything cited below is in the
repo except where explicitly marked LIVE-CONTAINER-ONLY.

---

## Decision requested

**Rule: APPLY / DO NOT APPLY / APPLY MODIFIED (say exactly how) / DIFFERENT ACTION FIRST.**

Proposed control: add a warning to `scripts/apply-directive.sh` (in the separate ops repo
`~/projects/autocompany-deploy`, not this one) that scans the directive body for
permanence-claiming language — "standing", "non-negotiable" and similar — and, when found, asks
whether the rule was also added to `PROMPT.md`.

Then say what would change your ruling and name anything material the pack failed to consider.

## 1. The mechanism, and today's failure

`memories/human-directive.md` is a **single slot**. Every writer overwrites the whole file; there
is no append, no merge, no diff shown to the writer.

Today a check found **seven rules** that everyone — operator and assistant — had been treating as
standing, present in **neither** `PROMPT.md` nor `CLAUDE.md`: legal-persons-only (gerçek kişi
excluded even inside an iş ortaklığı), the G2 12-month recency window, the operator's OPTION A
authorization, the pool-shape condition before a first send, the named-mirror restriction, the
two EKAP hard stops (no signed-API replication, no login), and the WTP wording. They existed only
inside successive directive bodies. Each new directive deleted the previous one's copy; they
survived only because the author retyped them under a heading like "Standing rules (unchanged,
non-negotiable)".

They are now in `PROMPT.md` under `### TENDER TRACK STANDING RULES` (commit `d5c6e91`) and
anchored in the assembled-prompt invariant (`scripts/core/auto-loop.sh`,
`REQUIRED_PROMPT_GUARDRAILS`). **The instance is fixed. The mechanism is not.**

Nothing errored while those rules were absent. The company did not in fact violate them in the
cycle observed, but it did source a `KararNo` from `ihaledanismani.com` — a mirror named as
off-limits in directives and named in no standing file at all at that moment.

## 2. OBSERVED — verifiable in this repo

**There are THREE writers of the single slot, and the proposal guards one:**

| # | Writer | Path | Backs up first? |
|---|---|---|---|
| 1 | Assistant / operator CLI | `apply-directive.sh:38` — `base64 -d > /app/memories/human-directive.md` (ops repo) | **No** |
| 2 | Cockpit Director panel | `dashboard/server.py` `write_directive()` — docstring: *"Overwrites any previous one."* | **No** |
| 3 | Analyst auto-promotion gate | `scripts/analyst/promote_directive.py:47` — `BACKUP_DIR = APP/"memories"/"human-directive-backups"` | **Yes** |

The proposal modifies writer 1 only.

- `dashboard/server.py:42` — `DIRECTIVE_FILE = REPO_ROOT / "memories" / "human-directive.md"`.
- Writer 1's output IS recoverable in practice, because those directive bodies are committed to
  the ops repo (`~/projects/autocompany-deploy/directives/`, e.g. commits `33d1613`, `20b2b82`,
  `b84eceb`, `4988ad6`, `4ba59f4` — all dated 2026-07-29). Writer 2's is not committed anywhere.
- LIVE-CONTAINER-ONLY: `/app/memories/human-directive-backups/` holds exactly **one** file,
  `human-directive-20260727T115247Z.md`, i.e. writer 3 has fired once and writers 1 and 2 have
  left no backups at all.

**The consumer side already has an enforcement pattern that works.** `auto-loop.sh` refuses to
start a cycle unless the assembled `FULL_PROMPT` still contains named guardrail literals, and
follows two gates into `PROJECT_EVALUATION_FRAMEWORK.md` when they were moved out of the prompt.
That check is deterministic, runs every cycle, and blocks rather than warns.

## 3. INFERRED — reasoning, check it

- A warning on writer 1 catches the assistant's own path, which is the path that has been
  disciplined so far (rules were retyped every time, correctly). The paths with no such habit —
  the operator clicking the cockpit panel, the analyst's automated promotion — stay unguarded.
- Keyword detection on "standing"/"non-negotiable" will fire on nearly every directive written in
  the current house style, because those directives all carry a "Standing rules (unchanged,
  non-negotiable)" recap section by convention. A control that fires ~always is a control that
  gets acknowledged reflexively.
- Conversely, a genuinely new permanent rule might be phrased without either keyword ("from now
  on", "never", "always", "going forward"), so the detector's misses are exactly the dangerous
  case: a NEW rule, not a recap.

## 4. UNKNOWN — left standing

- How often writer 2 (cockpit) is actually used for rule-bearing text versus one-off tasking.
  Not measured.
- Whether the operator wants directives to be able to carry permanent rules at all, or whether
  the correct model is "directives are tasks; rules only ever change via `PROMPT.md`". This is a
  policy question the pack cannot settle.
- Whether an interactive prompt is even reachable on writer 1's path in every invocation
  (it is run non-interactively by the assistant; a `read`-based confirmation may hang or be
  auto-skipped). Not tested.
- Whether any rule is currently living only in a directive right now, after today's fix. Not
  re-swept.

## 5. The case FOR the proposal

- It is cheap, local, and touches nothing the loop depends on.
- It attacks the moment of loss — the write — rather than trying to detect absence later.
- Today's seven-rule finding was discovered by accident, from noticing a mirror domain in a cycle
  summary. Any control beats accident.

## 6. The case AGAINST — argue the kill properly

- **It guards 1 of 3 writers**, and arguably the one least likely to fail, since that path's
  operator has retyped the rules correctly every time and now also writes them into `PROMPT.md`.
- **It warns rather than blocks**, in a system whose one demonstrably effective control
  (the assembled-prompt invariant) blocks.
- **It fires on almost every directive** given the current house style, so it trains the reader to
  dismiss it — and its misses are precisely the novel-rule case it exists for.
- **It lives in a different repository** from the rules it protects, so a clone of this repo has
  neither the control nor any trace of it.
- **A fourth option the pack should have weighed**: state in `PROMPT.md` that a directive may not
  create standing rules at all — directives are tasks, `PROMPT.md` is law — and have the loop
  itself flag a directive that claims permanence. That moves the control to the consumer side,
  where the working pattern already lives, and covers all three writers at once.

## 7. Known silent-failure modes in this system — check for analogues

All four shipped and ran undetected; the pattern is plausible-looking logic never exercised
against reality:
- an engine kill-switch that matched auth phrases anywhere in a cycle transcript, so a successful
  cycle disabled its own engine by writing "401 unauthorized" in a document;
- an operator-authorization verifier that truncated its parse window at 1000 chars and at the
  first `OPREQ-` substring, silently discarding a valid authorization;
- a content hash specified in prose rather than code, so two honest implementations disagreed;
- a section-size measurement whose parser ignored fenced code blocks, nearly shipping an edit that
  would have removed the WTP hard stop by default.

For the proposal: **what is its analogous silent failure, and what observable signal would reveal
it?**

## 8. Assembler's disclosure

The assembler proposed this control, and the control would guard the assembler's own path — the
one path already behaving correctly — while leaving the operator's cockpit path and the automated
promotion path unguarded. The assembler is also the author of the seven-rule loss being remedied:
six directives were applied today, each silently dropping the previous body, and the rules
survived only by the assembler's own retyping. Weigh whether the proposal is scoped to where the
risk is, or to where the proposer is.

---

# STATUS UPDATE — second adjudication round (same day, later)

The first round was adjudicated and **its ruling was DIFFERENT ACTION FIRST**: do not ship the
keyword-warning control in any form, and do four things in order instead. Steps 1 and the
invariant repair are now DONE. **This round rules on steps 2, 3 and 4 only.**

## Disclosure about the previous adjudication — read this first

The first round was adjudicated by a **Claude Opus subagent**, i.e. the same model family as the
assembler. It had no conversation context and only the pack plus repo access, so what it provided
was **context independence, not model independence**. The operator considers that insufficient and
has directed that adjudication be done by a **different model family**. Treat the previous
ruling as informed opinion from a related mind, not as an independent check — and say so if you
think it was wrong.

## What changed since the first pack (all verifiable in this repo)

- **Step 1 (re-sweep) DONE.** `scripts/ops/directive-rule-sweep.py`, now committed, walks every
  directive body and reports rule-shaped lines whose distinctive phrases do not survive in
  `PROMPT.md` / `CLAUDE.md` / `PROJECT_EVALUATION_FRAMEWORK.md`. First run: 30 bodies, 192
  rule-shaped lines, 38 flagged, nearly all obsolete or one-off task text. **Two were real:**
  - *"Do not relax a gate to achieve spread"* — genuinely absent, and absent because of wording
    the assembler added the same day: the pool-shape condition reads as pressure to widen the
    pool and nothing stated the complement. Now in `PROMPT.md` (commit `41ac2c5`).
  - The Arkenom no-exclusion-claim constraint — **obsolete, not lost**; its premise (that firm's
    G1 rested on a competitor mirror) was superseded when the bridge established G1 from the
    authority's decision text.
  - Checked and explicitly NOT a finding: an old directive says checkout attempts do not activate
    *exploitation* while `PROMPT.md` counts a priced fake-door with checkout attempts as WTP
    evidence for the *build* gate. Different gates, deliberately different bars.
- **Finding #4 from the first ruling (the `$CONSENSUS` hole) FIXED** (`41ac2c5`). Each guardrail
  is now checked against `PROMPT.md` **directly** first, and separately against the assembled
  prompt so an assembly-drop is still caught. Verified: section-deleted-but-consensus-name-drops
  it now BLOCKS; assembly-drop still BLOCKS.
- **The first pack was itself unreachable, exactly as its adjudicator complained.** It was moved
  to `docs/devops/` to escape the `memories/*` ignore — but `.gitignore:183-185` ignores
  `docs/*/*` too, with individually allowlisted exceptions. Fixed: `.gitignore:193` now keeps
  `docs/devops/decision-pack-*.md`, so this file is in the repo you are reading.
- **The backup-durability ambiguity is RESOLVED, and it favours step 3.** `/app/memories` is a
  named Docker volume (`z12a992i3ty202zezspij2fn-ac-memories`), and
  `human-directive-backups/human-directive-20260727T115247Z.md` has survived **eight redeploys
  today**. So "exactly one backup file" means writer 3 has fired once — not that the directory
  gets wiped. Backups written there are durable.
- **The first ruling's writer census was confirmed by measurement.** Five writers, not three.
  `PROMPT.md:18-19` instructs the loop's own model to edit the file every cycle. And
  `scripts/analyst/opportunity-analyst.sh:88-102` snapshots the file, then unconditionally
  restores the snapshot after the Codex run(s) — a window of up to ~50 minutes in which a
  directive applied by another writer is silently reverted, logged as *"restored
  human-directive.md (analyst must not write it)"*, which describes the opposite of what
  happened. **Checked: that line has never appeared in any log**, and today's analyst run (08:29)
  preceded every directive applied (from 12:37). Real hazard, never fired.

## The three proposals now before you

- **STEP 2 — the declaration.** State in `PROMPT.md` that a directive is a TASK and may not create
  standing rules — `PROMPT.md` is law — and add that statement's literal to
  `REQUIRED_PROMPT_GUARDRAILS` in `scripts/core/auto-loop.sh` so its removal blocks a cycle.
  Open policy question the assembler cannot settle: **should a directive be able to carry a
  permanent rule at all?** If yes, the declaration must be reworded from a prohibition to an
  obligation — a directive creating a standing rule must land it in `PROMPT.md` in the same
  change.
- **STEP 3 — back up before every write.** ~3 lines each in `dashboard/server.py`
  `write_directive()` and the ops-repo `apply-directive.sh`, writing into the
  `memories/human-directive-backups/` directory `scripts/analyst/promote_directive.py:47` already
  creates. No keyword matching, so it cannot miss the novel-rule case; no prompt, so it cannot be
  reflexively dismissed. Converts silent unrecoverable loss into silent recoverable loss.
- **STEP 4 — a consumer-side recorder.** If a detector is still wanted, put it on the loop side
  and have it RECORD that a directive claimed permanence, not ask a human about it.

Rule on each: **APPLY / DO NOT APPLY / APPLY MODIFIED (say exactly how) / DIFFERENT ACTION
FIRST.** Note that none of the three addresses the two highest-risk writers (the loop's own model
edit, and the analyst restore race) — say whether that is the real gap.

## Assembler's disclosure, this round

The assembler wrote the wording that created one of the two real sweep findings, shipped the
invariant hole being repaired, put two consecutive adjudication packs where their adjudicator
could not read them, and described the previous adjudicator as "independent" when it shared the
assembler's model family. Every item above is the assembler's own error found by someone else.
Weigh the pack's framing accordingly.
