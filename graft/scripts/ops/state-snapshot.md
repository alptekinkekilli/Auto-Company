# scripts/ops/state-snapshot.py

One-call cycle state snapshot that collapses the per-cycle probe fan-out into a single turn, printing directive/opreq/bridge/send/reply status plus a DELTA line against the previous snapshot so an unchanged world can be dismissed in one glance.

- api_key · function · L57-L67 — Resolves the Airtable API key from the environment, falling back to the runtime.env file so network probes can authenticate without a hardcoded secret.
- directive_state · function · L70-L78 — Reads the human directive file and returns its Status section plus a sha16 fingerprint used purely for change detection.
- opreq_open · function · L81-L93 — Scans the operator-requests ledger and returns the ids of blocks whose Status is OPEN, so the cycle knows which requests still need work.
- bridge_pending · function · L96-L118 — Counts PENDING rows in a bridge table via narrow pageSize=1 pages carrying only record ids, returning the count or an inline ERROR string.
- run_tool · function · L121-L130 — Runs a sibling ops script as a subprocess and returns its trimmed output, converting any failure into an inline ERROR string so the probe never raises.
- main · function · L133-L208 — Orchestrates the whole snapshot: gathers all field values, prints them compactly, computes a DELTA against the previous snapshot (excluding errored/skipped fields), and persists the new state.
