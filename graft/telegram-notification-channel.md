---
name: Telegram notification channel
slug: telegram-notification-channel
type: system
sources:
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
sources_digest: 3dc173f8889cdab53470b50d79d2518beedb357a6bcbc9c68f009fdbd555a439
links:
  - to: operator-escalation-gate
    relation: uses
    description: operator_request_notify.py sends notifications through this script.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash wrapper around the Telegram Bot API that is safe to call unconditionally: exits silently if credentials are unset, never returns non-zero, truncates messages to 3900 chars, and disables web page previews. Used by nearly every watcher and gate in the system as the operator alerting channel.

## Related

- uses [[operator-escalation-gate]] — operator_request_notify.py sends notifications through this script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
