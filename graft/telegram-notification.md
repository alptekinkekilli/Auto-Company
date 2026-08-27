---
name: Telegram notification
slug: telegram-notification
type: system
sources:
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
sources_digest: 3dc173f8889cdab53470b50d79d2518beedb357a6bcbc9c68f009fdbd555a439
links:
  - to: auto-company-loop-core
    relation: part_of
    description: Core notification utility used across the loop and ops scripts.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The shared real-time operator notification channel (telegram-notify.sh), safe to call unconditionally: exits silently if tokens are unset, never returns non-zero, truncates to 3900 chars, and disables web previews. Most ops watchers and the loop shell out to this script with credentials from logs/runtime.env.

## Related

- part of [[auto-company-loop-core]] — Core notification utility used across the loop and ops scripts.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
