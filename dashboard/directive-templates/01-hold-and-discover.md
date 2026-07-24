Status: ACTIVE
Issued: <FILL: YYYY-MM-DD>
Scope: HOLD <FILL: candidate name> pending <FILL: blocker>; make continuous opportunity discovery the primary activity.

## Primary activity this directive sets

Continuous opportunity discovery. While the item(s) in "Blocked / Pending Work"
below are parked, the loop's main autonomous work each cycle is bounded
opportunity-discovery scans — NOT re-auditing the frozen item(s).

## Blocked / Pending Work (the company must know these are parked and WHY)

- <FILL: candidate name> — status **HOLD**.
  - Blocked on: <FILL: e.g. $549 iyzico payment link>.
  - Why: <FILL: e.g. link is in iyzico onboarding/KYC — website-criteria review + identity/contract approval, days, operator-run>.
  - Owner to unblock: <FILL: operator / who>.
  - Unblock when: <FILL: the concrete condition, e.g. a live hosted payment link exists>.
  - Preserve intact (do NOT archive/dismantle/repurpose): <FILL: assets, e.g. Airtable Staging-QA Outreach + Intake + Sales Assets + Call Script, report template>.
  - Tracking: <FILL: Linear issue, e.g. APP-226>.
  - Registry: keep this candidate **Selected — status HOLD**; do not re-propose its axis.
  - While HOLD: NO outreach, payment request, qualified-contact work, staging access, fulfillment, or delivery for it.

<FILL: add more blocked items the same way, or delete this line if only one.>

## How discovery runs (framework-gated, every scan)

- Load `memories/candidate-registry.md` FIRST. Dedup by axis = (buyer × delivery-shape × price-point). Skip any axis in Selected / Archived / Pending (the HELD candidate's axis included); LOG what you excluded and why.
- Every surfaced candidate needs: buyer, delivery shape, price point, and the single cheapest willingness-to-pay test. Reject deadline/trend/regulation-only bets per `PROJECT_EVALUATION_FRAMEWORK.md`.
- Add qualified new candidates to `## Pending Queue`. Let the Opportunity Analyst score them, compare against the company's own pick, and write its directive draft for operator review. Keep scanning across cycles — do not stop after one scan.

## Guardrails (unchanged)

- HARD STOP for EVERY candidate: no product/software build before a real WTP signal (payment, pre-order, paid pilot, or priced fake-door with actual checkout attempts). Only permitted build = the cheapest WTP test (priced fake-door on Cloudflare Pages via the `cloudflare-pages-deploy` skill; never Vercel or this host).
- No autonomous outreach, payment action, staging access, or delivery for ANY candidate. Munger veto intact. Do NOT start any candidate's build without a NEW authorizing directive.

## Completion

Stays in effect (do not mark terminally done and revert to auditing the frozen item) until the operator either (a) clears the blocker and issues an un-HOLD directive, or (b) selects a different candidate. Discover every cycle until then.
