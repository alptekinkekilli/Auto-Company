---
name: Airtable Queue Watchers
slug: airtable-queue-watchers
type: system
sources:
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
sources_digest: 305298ddead7a83d752c5e7b584d481e97d3fa1fb28246cc2a1a8904e404439a
links:
  - to: outreach-eligibility-evidence
    relation: uses
    description: Both read the same outreach/registry Airtable tables.
  - to: telegram-notification-channel
    relation: uses
    description: Both notify via telegram-notify.sh.
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

Advisory watchers that tell an operator when Airtable-backed queues need attention. reply-watch.py classifies replies, delivery failures, and silence (superseding a later Sent over an earlier failure), alerting once per outcome. registry-queue-watch.py reports PENDING bridge rows (resolvable with ~1 CAPTCHA each) and Outreach rows Held on attribution that never got a bridge request, matching firms by first word of legal title. Both are strictly read-only and throttle via state files.

## Related

- uses [[outreach-eligibility-evidence]] — Both read the same outreach/registry Airtable tables.
- uses [[telegram-notification-channel]] — Both notify via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
