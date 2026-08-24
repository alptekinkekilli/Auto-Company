Status: ACTIVE
Scope: Blocker cleared — un-HOLD the currently held candidate and run its cheapest willingness-to-pay validation.

## Primary activity this directive sets

Un-HOLD the candidate that `memories/candidate-registry.md` currently records
under `## Selected` with status HOLD, and move it back to the active validation.
Its blocker is resolved; the newly available resource is whatever
`memories/consensus.md` (`## Next Action` / the latest operator-channel note)
records as having changed. Read those first — do not assume from memory — and
state in your first cycle which blocker you understood to be cleared, so a
mistaken un-hold is visible immediately instead of three cycles later.

## The validation to run

Take every parameter from the candidate's own registry row and the offer material
already built for it — buyer, offer, price, channel, the WTP test and its success
gate, the cohort size and the time window. They were defined when the candidate
was selected and are NOT re-opened by this directive. If a parameter is missing or
ambiguous, stop and open an OPREQ rather than inventing one.

Use the assets that already exist (Airtable outreach rows, intake, sales assets,
call script, report template). Do not rebuild them.

## Blocked / Pending Work

Anything else still parked is whatever the registry and `## Awaiting Operator`
list as HOLD/WAITING. Leave those parked, preserve their assets, do not
re-propose their axes.

## Guardrails (unchanged)

- Dispatch stays behind `send-gate.py` ALLOW with its caps; the operator's own
  gates and the standing outreach rules are unchanged by this directive.
- HARD STOP still applies to product BUILD: this authorises running the paid
  validation, NOT building product software. No production credentials, real card
  data, or customer PII — staging/synthetic/test paths only.
- WTP evidence means a real, settled, non-refunded payment from a real unrelated
  buyer. Test-mode transactions never count.
- Registry: set this candidate to **Selected — status ACTIVE (validating)**.
  Munger veto intact.

## Completion

Stays in effect until the validation reaches a terminal result (GO / PIVOT /
NO-GO / UNKNOWN per its own pre-registered rule) or the operator issues a new
directive. A quiet inbox is not a terminal result.
