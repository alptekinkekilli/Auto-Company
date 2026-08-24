status: ACTIVE
Scope: Wowcar 2.0 ONLY — document/ledger upkeep, no new gate work. The Tender Track
remains frozen historical state.

## Decision

Hold the program at its current state. Each cycle: read the pre-run state snapshot;
if DELTA is none and no §16 weekly report is due, write ONE confirming line to
`memories/consensus.md` and end the cycle — an empty cycle is the CORRECT output.
If DELTA names a change, process ONLY that change (directive, OPREQ resolution,
auditor report, Wowcar source-set, operator decision) and end.

## Authorization

Authorized: ledger/receipt upkeep, processing PENDING OPREQ resolutions, the §16
weekly report when due.

Not authorized: new gate work; any §15 sponsor-gated act; any Tender Track work;
discovery of any kind.

## Completion

No completion condition — this directive governs until superseded by a new operator
directive. Never mark it DONE from a quiet cycle.
