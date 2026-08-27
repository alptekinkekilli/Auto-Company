---
name: Reply watch
slug: reply-watch
type: system
sources:
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
sources_digest: 6ad06dbf2e8da6c0382ddefb20201d3052850087e1679f79278d0ff2d667c76c
links:
  - to: airtable-access-layer
    relation: uses
    description: Reads outreach records from the Ihale Outreach table.
  - to: telegram-notification
    relation: uses
    description: Notifies via telegram-notify.sh.
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

Operator alerting script that watches Airtable outreach records for three outcome classes — a reply, a delivery failure, or silence after a window — and notifies via Telegram. Advisory only (never writes back), treats delivery failure as distinct from silence, and applies a supersession rule where a later 'Sent' entry overrides an earlier failure. Uses a local state file so each row alerts once per outcome.

## Related

- uses [[airtable-access-layer]] — Reads outreach records from the Ihale Outreach table.
- uses [[telegram-notification]] — Notifies via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
