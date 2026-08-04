Status: ACTIVE
Scope: HOLD the current Active Validation; make bounded opportunity discovery the primary activity while it is parked.

## Primary activity this directive sets

Continuous, framework-gated opportunity discovery. While the parked item(s) below
wait, the loop's main autonomous work each cycle is a bounded discovery scan —
NOT re-auditing the frozen item(s).

## What is parked, and how to know (derive it; nothing here is filled in by hand)

Read the company's own records each cycle and treat THOSE as authoritative:

- `memories/candidate-registry.md` → `## Selected` is the Active Validation and
  carries its status. Put it on **HOLD** and keep it there.
- `memories/consensus.md` → `## Next Action` and `## Awaiting Operator` name what
  it is blocked on and who unblocks it.
- The open OPREQ register → anything waiting on an operator decision.

For every parked item: preserve its assets intact (do NOT archive, dismantle or
repurpose them), keep the Linear track issue recorded in its registry row, do not
re-propose its axis, and run NO outreach, payment request, qualified-contact work,
staging access, fulfillment or delivery for it while it is held.

## How discovery runs (framework-gated, every scan)

- Load `memories/candidate-registry.md` FIRST. Dedup by axis = (buyer × delivery
  shape × price point). Skip any axis already in Selected / Archived / Pending —
  the held candidate's axis included — and LOG what you excluded and why. No
  silent skipping.
- Aim for ~10 distinct new candidates per scan. Each needs a buyer, a delivery
  shape, a price point, and the single cheapest willingness-to-pay test. Reject
  deadline-, trend- or regulation-only bets per `PROJECT_EVALUATION_FRAMEWORK.md`.
- Add qualified candidates to `## Pending Queue`. The Opportunity Analyst scores
  them, compares them against the company's own pick and drafts a directive for
  operator review. Keep scanning across cycles — do not stop after one scan.

## Guardrails (unchanged)

- HARD STOP for EVERY candidate: no product/software build before a real WTP
  signal (payment, pre-order, paid pilot, or priced fake-door with actual checkout
  attempts). The only permitted build is the cheapest WTP test itself (priced
  fake-door on Cloudflare Pages via the `cloudflare-pages-deploy` skill; never
  Vercel, never this host).
- No autonomous outreach, payment action, staging access or delivery for ANY
  candidate. Munger veto intact. No candidate build without a NEW authorizing
  directive.

## Completion

Stays in effect until the operator issues a different directive — typically
un-holding the parked candidate or selecting a new one. Do not mark it DONE from
a quiet cycle or a finished scan, and do not drift back to auditing frozen work.
