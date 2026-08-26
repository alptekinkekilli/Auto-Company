---
name: ops-script-test-harness
slug: ops-script-test-harness
type: concept
sources:
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: 47d9496c5bfa8b836635036ee67977651a54d2cdeece22479df2054bcff4df9c
links:
  - to: reply-watch
    relation: validates
    description: The harness drives reply-watch's regression suite.
  - to: send-gate
    relation: validates
    description: The harness drives send-gate's 20-scenario suite.
  - to: state-snapshot
    relation: validates
    description: The harness drives state-snapshot's DELTA tests.
  - to: tool-usage-audit
    relation: validates
    description: The harness drives tool-usage-audit's idempotence tests.
  - to: turn-audit
    relation: validates
    description: The harness drives turn-audit's boundary tests.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Shared convention across the ops test suites: synthetic fixtures built with python3, run()/check()/contains/absent helpers, a fail counter, mktemp working dirs with trap cleanup, and assertions on stdout strings. Tests run the target script offline with network calls stubbed so guards are tested as pure policy.

## Related

- validates [[reply-watch]] — The harness drives reply-watch's regression suite.
- validates [[send-gate]] — The harness drives send-gate's 20-scenario suite.
- validates [[state-snapshot]] — The harness drives state-snapshot's DELTA tests.
- validates [[tool-usage-audit]] — The harness drives tool-usage-audit's idempotence tests.
- validates [[turn-audit]] — The harness drives turn-audit's boundary tests.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
