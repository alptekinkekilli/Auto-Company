---
name: registry-queue-watch
slug: registry-queue-watch
type: file
sources:
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
sources_digest: 22b71b743c7143d7cb116d708315bce263910e4b5333b9fd70f6159da59b2285
links:
  - to: telegram-notify
    relation: uses
    description: Sends queue-backlog alerts via the shared Telegram script.
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

Advisory watcher telling operator when a MERSİS session is worth their time. Reads Registry Bridge, EKAP Bridge, Ihale Outreach tables. Reports two distinct problems: PENDING bridge rows resolvable with ~1 CAPTCHA each, and Outreach rows Held on attribution that never got a bridge request queued. Strictly read-only. Matches firms by first word of legal title (bridge/outreach spell long names differently). Treats EKAP and MERSİS pending rows as one shared scarce resource.

## Related

- uses [[telegram-notify]] — Sends queue-backlog alerts via the shared Telegram script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
