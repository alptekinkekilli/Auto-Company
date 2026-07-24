Status: ACTIVE
Issued: <FILL: YYYY-MM-DD>
Scope: Make continuous opportunity discovery the primary activity; carry the standing blocked/pending register.

## Primary activity this directive sets

Continuous opportunity discovery. Each cycle's main autonomous work is a bounded
opportunity-discovery scan that surfaces NEW, distinct candidates the company
could validate. Do not stall on, or re-audit, the parked items below.

## Blocked / Pending Work (the company must know these are parked and WHY)

<FILL: list every item currently waiting, or write "None." For each:>
- <item / candidate> — status **<HOLD / WAITING>**.
  - Blocked on: <FILL>. Why: <FILL>. Owner: <FILL>. Unblock when: <FILL>.
  - Preserve intact: <FILL: assets not to touch>. Tracking: <FILL: Linear issue>.
  - Registry: keep **Selected — status HOLD**; do not re-propose its axis; no outreach/payment/delivery while parked.

## How discovery runs (framework-gated, every scan)

- Load `memories/candidate-registry.md` FIRST. Dedup by axis = (buyer × delivery-shape × price-point). Skip any axis in Selected / Archived / Pending; LOG exclusions + why (no silent skipping).
- Aim for ~<FILL: N, e.g. 10> distinct new candidates per scan, each with buyer, delivery shape, price point, and the single cheapest willingness-to-pay test. Reject deadline/trend/regulation-only bets per `PROJECT_EVALUATION_FRAMEWORK.md`.
- Add qualified candidates to `## Pending Queue`; the Opportunity Analyst scores them, compares to the company's own pick, and writes a directive draft for operator review. Keep scanning across cycles.

## Guardrails (unchanged)

- HARD STOP for EVERY candidate: no build before a real WTP signal. Only permitted build = the cheapest WTP test (priced fake-door on Cloudflare Pages via the `cloudflare-pages-deploy` skill; never Vercel or this host).
- No autonomous outreach, payment action, staging access, or delivery. Munger veto intact. No candidate build without a NEW authorizing directive.

## Completion

Stays in effect until the operator issues a new directive (e.g. selecting a candidate to validate, or un-HOLDing a parked one). Discover every cycle until then.
