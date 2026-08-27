---
name: Directive staleness watcher
slug: directive-staleness-watcher
type: system
sources:
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
sources_digest: 2da49c6c22e53f06775d58264310e950958b2bae6d54fa684cf37a2c50d95a4d
links:
  - to: human-directive-writer
    relation: validates
    description: >-
      Reads the directive's ## Status and ## Updated sections to judge
      staleness.
  - to: telegram-notification
    relation: uses
    description: Sends staleness alerts via telegram-notify.sh.
generator:
  version: 1
covers:
  - symbol: read_directive
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L40-L56'
  - symbol: last_line_matching
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L59-L66'
  - symbol: main
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L69-L165'
---
<!-- context:generated:start -->
## Summary

Operational watcher that alerts when the human directive remains PENDING beyond a threshold, because the completion clause can only be satisfied by market evidence or an explicit terminal decision — neither of which the company can produce alone. Never edits or clears the directive; only reports, with a persisted last_notified timestamp to avoid spamming a 15-minute cron.

## Related

- validates [[human-directive-writer]] — Reads the directive's ## Status and ## Updated sections to judge staleness.
- uses [[telegram-notification]] — Sends staleness alerts via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
