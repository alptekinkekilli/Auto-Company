---
name: ops_watchers
slug: ops-watchers
type: system
sources:
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
  - path: tests/test_registry_queue_watch.sh
    hash: 0c823a0b115d8fb57d7a64e25cb89f725943078e58504a22aa5306a416ac6668
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
sources_digest: a6fc8b7d1831fd9c9f2b5c14a413a15936033f233eca7de4d59f44ad6846e551
links:
  - to: operator-request-notify
    relation: uses
    description: >-
      Shares the same state-file persistence and dedup conventions for
      suppressing duplicate alerts.
generator:
  version: 1
covers:
  - symbol: api_key
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L48-L58'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L61-L77'
  - symbol: main
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L80-L215'
  - symbol: api_key
    kind: function
    at: 'scripts/ops/reply-watch.py:L46-L56'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/reply-watch.py:L59-L74'
  - symbol: notify
    kind: function
    at: 'scripts/ops/reply-watch.py:L77-L91'
  - symbol: first_ts
    kind: function
    at: 'scripts/ops/reply-watch.py:L94-L99'
  - symbol: hours_since
    kind: function
    at: 'scripts/ops/reply-watch.py:L102-L112'
  - symbol: main
    kind: function
    at: 'scripts/ops/reply-watch.py:L115-L142'
  - symbol: classify
    kind: function
    at: 'scripts/ops/reply-watch.py:L145-L223'
---
<!-- context:generated:start -->
## Summary

A family of scripts/ops watchers that classify and alert on external outcomes, each with a state file for dedup/cooldown and a --dry-run mode that writes no state. reply-watch.py classifies email replies/bounces/silence (72h threshold, lexicographic ISO timestamps, replies never also silent, silence phrased as observation not verdict). registry-queue-watch.py (APP-277) fires only above threshold and respects cooldown, distinguishing an empty bridge queue with many attribution-Held firms as a company gap (not operator gap) and detecting EKAP-only queues (a v1 blind spot).

## Related

- uses [[operator-request-notify]] — Shares the same state-file persistence and dedup conventions for suppressing duplicate alerts.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
