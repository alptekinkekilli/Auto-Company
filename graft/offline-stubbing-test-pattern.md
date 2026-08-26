---
name: offline stubbing test pattern
slug: offline-stubbing-test-pattern
type: concept
sources:
  - path: tests/test_registry_queue_watch.sh
    hash: 0c823a0b115d8fb57d7a64e25cb89f725943078e58504a22aa5306a416ac6668
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: fb4d1c88cf0d6743b62c63a031b2e823bed056a080b253c830296cd1e3808158
links:
  - to: ops-watchers-audit-scripts
    relation: validates
    description: >-
      The pattern is the mechanism by which these scripts' policies are
      verified.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Shared test technique: bash harnesses build synthetic fixtures and monkey-patch the Python scripts' network/IO boundaries (urllib.request.urlopen, air(), g4_live()) inside heredocs so every guard is exercised as pure policy with no live Airtable/G4. Assertions use contains/not_contains helpers over captured stdout, with mktemp + trap cleanup and a fail counter that exits non-zero on any failure.

## Related

- validates [[ops-watchers-audit-scripts]] — The pattern is the mechanism by which these scripts' policies are verified.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
