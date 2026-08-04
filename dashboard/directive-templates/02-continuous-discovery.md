Status: ACTIVE
Scope: Make bounded opportunity discovery the primary activity; carry the standing blocked/pending register.

## Primary activity this directive sets

Continuous opportunity discovery. Each cycle's main autonomous work is a bounded
scan that surfaces NEW, distinct candidates the company could validate. Do not
stall on, or re-audit, whatever is currently parked.

## What is parked, and how to know (derive it; nothing here is filled in by hand)

Read the company's own records each cycle and treat THOSE as authoritative:
`memories/candidate-registry.md` (`## Selected` and its status), `memories/consensus.md`
(`## Next Action`, `## Awaiting Operator`), and the open OPREQ register. Anything
listed there as HOLD/WAITING stays parked: preserve its assets, keep the Linear
track issue in its registry row, do not re-propose its axis, and run no
outreach/payment/delivery for it.

## How discovery runs (framework-gated, every scan)

- Load `memories/candidate-registry.md` FIRST. Dedup by axis = (buyer × delivery
  shape × price point). Skip any axis already in Selected / Archived / Pending and
  LOG what you excluded and why — no silent skipping.
- Aim for ~10 distinct new candidates per scan. Each needs a buyer, a delivery
  shape, a price point, and the single cheapest willingness-to-pay test. Reject
  deadline-, trend- or regulation-only bets per `PROJECT_EVALUATION_FRAMEWORK.md`.
- Add qualified candidates to `## Pending Queue`. The Opportunity Analyst scores
  them, compares them against the company's own pick and drafts a directive for
  operator review. Keep scanning across cycles.

## Guardrails (unchanged)

- HARD STOP for EVERY candidate: no build before a real WTP signal. The only
  permitted build is the cheapest WTP test itself (priced fake-door on Cloudflare
  Pages via the `cloudflare-pages-deploy` skill; never Vercel, never this host).
- WTP evidence means a real, settled, non-refunded payment from a real unrelated
  buyer; test-mode transactions never count.
- No autonomous outreach, payment action, staging access or delivery. Munger veto
  intact. No candidate build without a NEW authorizing directive.

## Completion

Stays in effect until the operator issues a new directive (selecting a candidate
to validate, un-holding a parked one, or switching to watch mode). Discover every
cycle until then.
