---
name: airtable
slug: airtable
type: concept
sources:
  - path: tests/test_registry_queue_watch.sh
    hash: 0c823a0b115d8fb57d7a64e25cb89f725943078e58504a22aa5306a416ac6668
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: f20deadfc568cd72560c2f1699cca6fbfa719c25ccd30c812c8c6ff32e864d85
links:
  - to: registry-ops
    relation: uses
    description: registry-queue-watch reads pending/held/EKAP records from Airtable.
  - to: reply-watch
    relation: uses
    description: reply-watch reads outreach outcome rows from Airtable.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The Airtable data source used by the ops watchers (registry-queue-watch, reply-watch, send-gate). Tests stub it by monkey-patching urllib.request.urlopen inside Python heredocs to inject deterministic fake records, so all guard/watcher logic is exercised as pure policy offline.

## Related

- uses [[registry-ops]] — registry-queue-watch reads pending/held/EKAP records from Airtable.
- uses [[reply-watch]] — reply-watch reads outreach outcome rows from Airtable.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
