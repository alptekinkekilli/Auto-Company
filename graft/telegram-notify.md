---
name: telegram-notify
slug: telegram-notify
type: file
sources:
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
sources_digest: 3dc173f8889cdab53470b50d79d2518beedb357a6bcbc9c68f009fdbd555a439
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Shared Telegram notification channel. Safe to call unconditionally: exits silently if token/chat unset, never returns non-zero. Truncates to 3900 chars (4096 limit), 15s curl timeout, disables previews.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
