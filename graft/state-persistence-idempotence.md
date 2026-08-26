---
name: state persistence & idempotence
slug: state-persistence-idempotence
type: concept
sources:
  - path: tests/test_registry_queue_watch.sh
    hash: 0c823a0b115d8fb57d7a64e25cb89f725943078e58504a22aa5306a416ac6668
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
sources_digest: 0c0a0b0c7aebb48438626b8712a2b34507e900ae1d7a8287decffb6bcd547526
links:
  - to: ops-watchers-audit-scripts
    relation: part_of
    description: >-
      The state-file behavior is implemented by each script and pinned by its
      test.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cross-cutting invariant across the ops scripts: every watcher/audit persists a JSON state file so repeated runs are idempotent and never re-alert on already-seen conditions. --dry-run must never write state; state is cleared when the underlying condition drains (e.g. queue empties) so the next backlog alerts immediately. Tool-usage-audit additionally re-audits rewritten cycle files (cycle counter resets on container restart) rather than deduping by filename, and backfills new cycle files.

## Related

- part of [[ops-watchers-audit-scripts]] — The state-file behavior is implemented by each script and pinned by its test.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
