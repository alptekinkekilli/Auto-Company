---
name: reply-watch
slug: reply-watch
type: file
sources:
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
sources_digest: 6ad06dbf2e8da6c0382ddefb20201d3052850087e1679f79278d0ff2d667c76c
links:
  - to: telegram-notify
    relation: uses
    description: Sends outcome alerts via the shared Telegram script.
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

Operator alerting script watching Airtable outreach records for reply, delivery failure, or silence after configurable window. State file ensures each row alerts once per outcome. Advisory — never writes back to Airtable, queues, or re-sends. Delivery failure distinct from silence, supersession rule: later 'Sent' overrides earlier failure.

## Related

- uses [[telegram-notify]] — Sends outcome alerts via the shared Telegram script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
