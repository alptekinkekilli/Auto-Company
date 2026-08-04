Status: ACTIVE
Scope: Adopt the top-ranked pending candidate as the active one and run its cheapest willingness-to-pay test.

## Primary activity this directive sets

Adopt as the active candidate whichever entry the Opportunity Analyst most
recently recommended (`memories/analysis-directive.md`) — or, if that report has
no live recommendation, the highest-ranked entry in `## Pending Queue` of
`memories/candidate-registry.md`. Name the one you adopted, and why, in your first
cycle's consensus line, so the choice is auditable rather than implicit.

Build ONLY the cheapest thing that can produce a real WTP signal. Not the product.

## The validation to run

- Axis: take buyer × delivery shape × price point from the candidate's own
  registry row. It must NOT overlap an axis already in Selected or Archived.
- Cheapest WTP test: a priced offer page with a real checkout or pre-order CTA,
  deployed with the `cloudflare-pages-deploy` skill (never Vercel, never this
  host). Use `frontend-design` before building it. Verify it returns HTTP 200 on
  its production URL before reporting it as live.
- Success signal: define it BEFORE shipping, in the registry row and in consensus,
  as a number and a deadline (how many priced checkout attempts or pre-orders, by
  when). A signal defined afterwards is not evidence.
- If the test returns no paid signal by its own deadline, record that and PIVOT or
  close it. Do not build the product anyway, and do not extend the deadline more
  than once without an operator directive.

## Blocked / Pending Work

Whatever the registry and `## Awaiting Operator` currently list as HOLD/WAITING
stays parked: preserve its assets, keep its Linear track issue, do not re-propose
its axis, no outreach/payment/delivery for it.

## How (framework-gated)

- Move the adopted candidate to `## Selected` in the registry with its Linear
  issue. Apply `PROJECT_EVALUATION_FRAMEWORK.md` to the decision and record the
  section numbers you relied on.
- Keep discovering on OTHER unrepresented axes only if capacity allows and no
  directive forbids discovery.

## Guardrails (unchanged)

- HARD STOP: no product/software build before the WTP signal above actually
  exists. The only permitted build is the WTP test itself.
- WTP evidence means a real, settled, non-refunded payment from a real unrelated
  buyer; test-mode transactions never count.
- Dispatch stays behind `send-gate.py` ALLOW with its caps. Munger veto intact.

## Completion

Stays in effect until the WTP test produces a terminal read (paid signal → GO to a
bounded build; no signal → PIVOT / NO-GO) or the operator issues a new directive.
