Status: ACTIVE
Scope: WATCH MODE — no discovery, no exploration, no source-mining. Keep existing work alive and cheap: Human Directive / OPREQ handling, replies, bridges, send-gate state, and closing out already-bounded tasks. Nothing new is started.

## Primary activity this directive sets

**Maintain, do not explore.** Each cycle: check whether anything the company is
already responsible for has MOVED, act on it if so, otherwise end the cycle.

An empty cycle is the CORRECT output here. It is not a failure and not a reason
to go looking for work. When nothing moved, say so in ONE line, update
`memories/consensus.md`, and end the cycle immediately.

## What each cycle may do (the whole list)

1. The pre-run state snapshot is already in the prompt. If its DELTA says nothing
   moved, do NOT re-verify anything — go to step 5.
2. Human Directive and OPREQ work, whenever either has something open.
3. Whatever the DELTA names as changed: a reply, an opt-out, a send-gate state, a
   Registry/EKAP Bridge result, a delivery failure, a newly-silent row. Handle it
   under the existing rules; nothing here authorises a send `send-gate.py` refuses.
4. CLOSING OUT a task that already has a written stop condition — finish it and
   record the verdict. Do not extend it or start its "next phase".
5. Update consensus with one line and end the cycle.

## Not allowed while this is in effect

- No opportunity discovery, no new candidate axes, no scanning or ranking.
- No new source-mining or feasibility reading, including sources that looked
  promising in an earlier cycle.
- No re-auditing frozen/archived work; no re-running suites "as a baseline".
- No new tooling, refactor or infrastructure work unless a Human Directive or an
  OPREQ asks for it by name.
- No build of any kind. Standing hard stops unchanged: WTP = a real settled
  payment; outreach only behind `send-gate.py` ALLOW with its caps; firm opt-outs
  permanent; price/payment/commitment questions stop and open an OPREQ.

## Blocked / Pending Work

Do not expect this list to be filled in by hand. Derive it each cycle from the
company's own records and treat THOSE as authoritative: `memories/candidate-registry.md`
(`## Selected` = the Active Validation and its status), `memories/consensus.md`
(`## Next Action`, `## Awaiting Operator`), and the open OPREQ register. Anything
listed there as HOLD/WAITING stays parked: preserve its assets, do not re-propose
its axis, no outreach/payment/delivery for it.

## Active validation

Whatever the registry currently records as the Active Validation, with its own
terminal date and stop gate. This directive does NOT change its verdict, offer,
caps or dates — it only bounds what the loop does while that validation waits.

**Dated obligations survive this directive.** Any deadline already recorded in the
previous directive, the registry or consensus — a terminal date, a demotion
boundary, a pre-registered outcome rule, an adjudication due date — still runs on
its own date. Executing one is CLOSING OUT a bounded task (allowed above), not new
work, and watch mode is never a reason to let a date pass unhandled. On the day,
do exactly what that obligation says and record the result; do not re-open the
decision or extend the date without an operator directive.

## If the loop was mechanically held

The operator may arm the mechanical hold (`logs/LOOP_HOLD`) on top of this
directive; that is a harder stop — no cycle runs at all. On resumption:

- The FIRST cycle after a hold is still a WATCH cycle. Act only on what the DELTA
  names. A long list of changes is a worklist, not permission to explore.
- Order: OPREQ → Human Directive → replies/opt-outs → bridge results → send-gate.
  One cycle may handle several; that is not a budget violation.
- Do not reconstruct what happened during the gap and do not audit the hold.
- Never write, clear or edit `logs/LOOP_HOLD` yourself — operator-only in both
  directions. If you believe the company should stop, say so in consensus and
  open an OPREQ.

## Cost expectation (part of the instruction, not a footnote)

Cycles here should be SHORT — a handful of tool calls when nothing moved. If a
cycle passes ~15 tool calls without the snapshot naming something changed, you
are exploring: stop and end the cycle.

## Completion

No completion condition of its own. It stays in effect until the operator issues
a different directive. Do NOT mark it DONE from a quiet cycle, an empty inbox, or
internal readiness.
