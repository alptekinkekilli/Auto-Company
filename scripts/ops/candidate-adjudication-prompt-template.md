# Template — adjudication brief for a candidate that passed economics

Auto Company decisions are not made by the operator on the operator's judgement alone. When a
candidate survives discovery and economics, it is escalated to an independent high-capability
model with an evidence pack, exactly as the 0-for-61 kill-pattern audit was (2026-07-25). The
company's job is to assemble that pack; the model rules; the operator then acts.

This is the template. The company fills it in and writes it to
`memories/decision-pack-<axis-id>.md` alongside the raw evidence file it references. Fill
every section — a missing section is a finding, so write "not available and why" rather than
deleting the heading.

---

## Decision requested

Should Auto Company spend its next authorized action on the cheapest real willingness-to-pay
test for this candidate, or not? Rule: **RUN WTP TEST / DO NOT RUN / RUN A DIFFERENT TEST
FIRST**, and say what would change your ruling.

## 1. The axis, stated precisely

- Stable axis ID, and the arm it came from (near-miss / remediation / control).
- Buyer × delivery shape × price point (the dedup key).
- The exact unit being sold, and what "done" means contractually — enumerated deliverables,
  source-population coverage, tests, evidence links, revision cap, sign-off. Not a downstream
  outcome the buyer hopes for.
- The triggering event that makes a buyer want this on a given day.

## 2. Evidence FOR, with primary sources

Every claim gets a link or a quote with its date. Separate what was OBSERVED from what was
INFERRED — the audit found inference repeatedly presented as observation.

- Observed buyer spend on this or an adjacent outcome (who, how much, where seen).
- Observed pricing of the credible alternatives.
- Observed demand signal: postings, bounties, complaint threads, marketplace listings.
- Where the money would arrive from, using an existing payment rail the company can list on.

## 3. Evidence AGAINST — argue the kill case properly

Write the strongest honest case that this dies, using the amended SEARCH REGIME definitions:

- Is there a NAMED substitute serving the same buyer, same trigger, same required inputs, and
  the same end-to-end acceptance unit at equal or lower total cost? Name it or state that
  none was found.
- Authority/licensing: is a licensed professional's judgement or sign-off legally required?
  (Ordinary commercial reliance is not.)
- Cold-start: does this need a two-sided network or reputation the company cannot seed?

## 4. Economics, bottom-up

Base and stress cases. Show the arithmetic, not just the conclusion: fulfillment time per
unit, cost per unit, price, gross margin, and what breaks the stress case. State every input
that is an estimate rather than a measurement.

## 5. What is still UNKNOWN

List explicitly. Under the amended regime UNKNOWN is a legitimate status, not a soft kill —
so name the unknowns that a WTP test would resolve and the ones it would not.

## 6. The proposed test

- The cheapest action that produces a REAL payment-intent signal (a real payment, pre-order,
  paid pilot commitment, or a priced fake-door with actual checkout attempts). Interest,
  signups, traffic, and "I'd use this" do not count.
- What it costs, how long it runs, and the pass/fail threshold set BEFORE running it.
- What a negative result would kill — the whole axis, or only this offer shape.

## 7. Instructions to the adjudicating model

- Judge each claim on its evidence, not on how well it is argued. This company writes
  persuasively; a 0-for-61 record went unquestioned for 32 cycles partly for that reason.
- Where a claim is plausible but unevidenced, say so rather than accepting it.
- Known failure modes in this system, offered so you can check for their analogues: a detector
  once matched the company's own prose about "billing" and "quota" and misread 43% of cycles;
  a cost field read `N/A` for hours and looked like "no data" rather than a broken pipe; an
  evidence extractor emitted axis titles with no bodies and was shipped as an evidence pack.
  Assume similar silent failures may exist in what you are being shown, and flag any you can
  detect.
- Constraints any recommendation must respect: no customers, no channel, no reputation, no
  proprietary data; cold outreach, payments and fulfillment are unauthorized without an
  explicit operator directive; WTP evidence precedes any build; the operator is one person.
- State what observation would prove your ruling wrong, and how quickly it could be seen.
