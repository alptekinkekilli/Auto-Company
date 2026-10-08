---
name: state snapshot and DELTA
slug: state-snapshot-and-delta
type: system
sources:
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: c4fec3f47231f04076a2c5e78da79a5f435a63bc80fda29f4240ad3959def8b5
links:
  - to: work-window
    relation: produces
    description: DELTA lines feed the work-window brake's open/closed decision
  - to: work-window-watchdog
    relation: produces
    description: DELTA lines feed the watchdog's empty-cycle detection
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

state-snapshot.py parses human-directive.md status/sha16, OPREQ open counts, and produces DELTA change-detection outputs (first-run, none, named changes, error exclusion). A missing ledger prints an error but still exits 0; errored fields are excluded from the next DELTA. All fields are local since a 2026-08-24 re-charter, with bridge/send/reply fields retired. The --skip-network path avoids network calls.

## Related

- produces [[work-window]] — DELTA lines feed the work-window brake's open/closed decision
- produces [[work-window-watchdog]] — DELTA lines feed the watchdog's empty-cycle detection
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
