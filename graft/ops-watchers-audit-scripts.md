---
name: ops watchers & audit scripts
slug: ops-watchers-audit-scripts
type: system
sources:
  - path: tests/test_registry_queue_watch.sh
    hash: 0c823a0b115d8fb57d7a64e25cb89f725943078e58504a22aa5306a416ac6668
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
sources_digest: ffd3747fae5f3d31a9d0423861a38376d48643edec51a2f586d5fea9e6a796cc
links:
  - to: offline-stubbing-test-pattern
    relation: validates
    description: >-
      These tests stub network calls (urllib.request.urlopen, air(), g4_live())
      to exercise the scripts as pure policy.
  - to: state-persistence-idempotence
    relation: implements
    description: >-
      Each watcher/audit writes a JSON state file (e.g.
      .registry-queue-state.json, logs/ state) so a second run suppresses
      duplicate alerts; --dry-run must never write state.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A family of Python operational scripts under scripts/ops that watch live state and emit Turkish-language alerts or audit trails: registry-queue-watch (fires only above threshold, respects cooldown, distinguishes company vs operator gaps), reply-watch (classifies replies/bounces/silence for outreach), send-gate (fail-closed refusal policy for outreach sends), state-snapshot (local-only DELTA change detection), tool-usage-audit (idempotent jcode NDJSON tool accounting), and turn-audit (turn-economy policy verdicts). All are driven by CLI flags (--app, --dry-run, --fixture) and persist state to JSON files under logs/ so repeated runs suppress duplicate alerts.

## Related

- validates [[offline-stubbing-test-pattern]] — These tests stub network calls (urllib.request.urlopen, air(), g4_live()) to exercise the scripts as pure policy.
- implements [[state-persistence-idempotence]] — Each watcher/audit writes a JSON state file (e.g. .registry-queue-state.json, logs/ state) so a second run suppresses duplicate alerts; --dry-run must never write state.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
