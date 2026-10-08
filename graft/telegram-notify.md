---
name: Telegram notify
slug: telegram-notify
type: system
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

Safe-to-call-unconditionally Telegram sender: exits silently if credentials are unset, never returns non-zero, truncates to 3900 chars (under the 4096 limit), disables web previews, 15s curl timeout. The shared notification channel used by nearly every watcher and gate in the system.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
