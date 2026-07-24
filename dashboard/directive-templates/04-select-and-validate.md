Status: ACTIVE
Issued: <FILL: YYYY-MM-DD>
Scope: Select <FILL: candidate name/# from the analyst pick or Pending Queue> as the active candidate and begin its cheapest willingness-to-pay test.

## Primary activity this directive sets

Adopt <FILL: candidate name> (e.g. the Opportunity Analyst's recommended pick / a `## Pending Queue` entry) as the active candidate. Build ONLY the cheapest thing that can produce a real WTP signal — not the product.

## Active validation

- Candidate: <FILL: name>. Axis: buyer <FILL> × delivery <FILL> × price <FILL>.
- Why this one: <FILL: one line — the analyst's reasoning or the operator's call>.
- Cheapest WTP test: <FILL: e.g. a priced fake-door landing page on Cloudflare Pages with a real checkout/waitlist CTA; measure actual checkout attempts / pre-orders>.
- Success signal that would justify a build: <FILL: e.g. >=N priced checkout attempts or >=M pre-orders within <days>>.
- First concrete step this cycle: <FILL: e.g. use the `cloudflare-pages-deploy` skill to ship the offer landing; use frontend-design first; verify it returns 200 live before reporting>.

## Blocked / Pending Work

<FILL: any items still parked (e.g. Candidate #4 on HOLD), or "None." Same format as the other templates — keep the company aware of what is waiting and why.>

## How (framework-gated)

- Update `memories/candidate-registry.md`: move this candidate to `## Selected` (with its Linear issue); it must be on an axis NOT overlapping an Archived entry. Keep discovering on OTHER unrepresented axes in the background if capacity allows.
- Apply `PROJECT_EVALUATION_FRAMEWORK.md`. If the WTP test returns no paid signal, record it and PIVOT — do not build the product anyway.

## Guardrails (unchanged)

- HARD STOP: no product/software build before the WTP signal above exists. The only permitted build is the WTP test itself (Cloudflare Pages via `cloudflare-pages-deploy`; never Vercel or this host). Verify any deploy is live (HTTP 200) before claiming it.
- No autonomous outreach, payment action, staging access, or delivery — human-execution gate stands. Munger veto intact.

## Completion

Stays in effect until the WTP test produces a terminal read (paid signal → GO to a bounded build, or no signal → PIVOT/NO-GO) or the operator issues a new directive.
