---
name: Telegram Notification Channel
slug: telegram-notification-channel
type: system
sources:
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: 875ac09d3881cc65a58be24ab4eb3cc263052e0fafa782d0a4d99a38657c4c96
links:
  - to: operator-escalation-notification
    relation: implements
    description: Provides the delivery mechanism those gates call.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The single real-time operator notification channel. telegram-notify.sh is safe to call unconditionally (silent no-op without tokens, never non-zero, truncates to 3900 chars). docker-prune-safe.sh pipes messages into the running container to read tokens from runtime.env rather than dot-sourcing it (values contain '|').

## Related

- implements [[operator-escalation-notification]] — Provides the delivery mechanism those gates call.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
