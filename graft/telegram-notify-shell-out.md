---
name: Telegram notify shell-out
slug: telegram-notify-shell-out
type: system
sources:
  - path: scripts/core/telegram-notify.sh
    hash: a6b475c3d6e94b205066d93a4054681477be96876b0f8eac60b47f13ab2573ef
sources_digest: 3dc173f8889cdab53470b50d79d2518beedb357a6bcbc9c68f009fdbd555a439
links:
  - to: airtable-ops-watchers
    relation: uses
    description: All watchers deliver alerts through this script.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The shared notification sink: scripts/core/telegram-notify.sh, invoked by all watchers and escalation scripts with tokens loaded from logs/runtime.env. Watchers degrade gracefully if the script or API key is missing.

## Related

- uses [[airtable-ops-watchers]] — All watchers deliver alerts through this script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
