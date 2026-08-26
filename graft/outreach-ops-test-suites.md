---
name: Outreach ops test suites
slug: outreach-ops-test-suites
type: system
sources:
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: 93663c3b0200b26d44d5e634fe641e1e354a96af7b384f7eef0c3201cec706ea
links:
  - to: outreach-ops-scripts
    relation: validates
    description: Each suite exercises one ops script's flags and invariants.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash regression suites (one per ops script) that build synthetic fixtures, run the target script via a run() helper, and assert on stdout with contains/absent helpers and a fail counter. They pin boundary values and real-incident regressions (Rayelsis, Arkenom, N.K.Y, Bilgi Birikim) to prevent silent recalibration drift, and stub network calls so policy is tested as pure logic.

## Related

- validates [[outreach-ops-scripts]] — Each suite exercises one ops script's flags and invariants.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
