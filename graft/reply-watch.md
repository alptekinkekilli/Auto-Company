---
name: reply-watch
slug: reply-watch
type: system
sources:
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
sources_digest: ce5714749921b9400cfaa17af0fe9932f3146e57178b31a75e3812be36b83d8e
links:
  - to: send-gate
    relation: uses
    description: >-
      Both consume the same outreach fixture/state conventions; reply-watch's
      Sent rows are the same events send-gate gates.
generator:
  version: 1
covers:
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

Classifies outreach email replies, bounces, and silence for five real firms, persisting state to suppress duplicate alerts and honoring a 72-hour silence threshold. Uses lexicographically comparable ISO timestamps; a replied row must never also be reported as silence, and a failure superseded by a later Sent is not a delivery problem.

## Related

- uses [[send-gate]] — Both consume the same outreach fixture/state conventions; reply-watch's Sent rows are the same events send-gate gates.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
