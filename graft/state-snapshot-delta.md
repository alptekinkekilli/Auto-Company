---
name: State snapshot DELTA
slug: state-snapshot-delta
type: concept
sources:
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: b22d6b1127d5b052b726fc0dc5a244376cf2f7f1b8d621a83596632c9199dcd2
links:
  - to: outreach-ops-scripts
    relation: part_of
    description: state-snapshot.py is one of the ops scripts.
  - to: outreach-ops-test-suites
    relation: validates
    description: test_state_snapshot.sh exercises the --skip-network path and DELTA logic.
generator:
  version: 1
covers:
  - symbol: file_sha16
    kind: function
    at: 'scripts/ops/state-snapshot.py:L54-L61'
  - symbol: directive_state
    kind: function
    at: 'scripts/ops/state-snapshot.py:L64-L72'
  - symbol: opreq_open
    kind: function
    at: 'scripts/ops/state-snapshot.py:L75-L87'
  - symbol: wowcar_sources
    kind: function
    at: 'scripts/ops/state-snapshot.py:L90-L104'
  - symbol: main
    kind: function
    at: 'scripts/ops/state-snapshot.py:L107-L166'
---
<!-- context:generated:start -->
## Summary

state-snapshot.py's change-detection: parses directive status/sha16 and OPREQ open counts, emits DELTA outputs (first-run, none, named changes, error exclusion), and excludes errored fields from the next DELTA. A missing ledger prints an error but still exits 0. All fields are local since a 2026-08-24 re-charter, with bridge/send/reply fields retired.

## Related

- part of [[outreach-ops-scripts]] — state-snapshot.py is one of the ops scripts.
- validates [[outreach-ops-test-suites]] — test_state_snapshot.sh exercises the --skip-network path and DELTA logic.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
