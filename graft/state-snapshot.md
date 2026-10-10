---
name: state snapshot
slug: state-snapshot
type: file
sources:
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: c4fec3f47231f04076a2c5e78da79a5f435a63bc80fda29f4240ad3959def8b5
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

state-snapshot.py computes DELTA change-detection with --skip-network path. Missing ledger prints an error but still exits 0; errored fields are excluded from the next DELTA. All fields are local since a 2026-08-24 re-charter; bridge/send/reply fields retired.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
