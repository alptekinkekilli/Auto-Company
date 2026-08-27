---
name: Registry queue watch
slug: registry-queue-watch
type: system
sources:
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
sources_digest: 22b71b743c7143d7cb116d708315bce263910e4b5333b9fd70f6159da59b2285
links:
  - to: airtable-access-layer
    relation: uses
    description: Reads the three Airtable tables via the REST API.
  - to: telegram-notification
    relation: uses
    description: Notifies the operator via telegram-notify.sh.
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
---
<!-- context:generated:start -->
## Summary

Advisory watcher that monitors Airtable queues to tell an operator when a MERSİS session is worth their time, addressing the gap where pending registry requests sat unnoticed. Reports two distinct problems: PENDING bridge rows resolvable with ~1 CAPTCHA each, and Outreach rows Held on attribution that never got a bridge request queued. Strictly read-only, matches firms by the first word of their legal title, and treats EKAP and MERSİS pending rows as one shared scarce resource.

## Related

- uses [[airtable-access-layer]] — Reads the three Airtable tables via the REST API.
- uses [[telegram-notification]] — Notifies the operator via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
