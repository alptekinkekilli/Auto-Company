---
name: directive-staleness-watch
slug: directive-staleness-watch
type: file
sources:
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
sources_digest: 2da49c6c22e53f06775d58264310e950958b2bae6d54fa684cf37a2c50d95a4d
links:
  - to: directive-writer
    relation: uses
    description: Reads the directive and its audit log produced by directive_writer.
  - to: telegram-notify
    relation: uses
    description: Sends staleness alerts via the shared Telegram script.
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

Operational watcher alerting when human-directive.md stays PENDING beyond threshold (12h), because completion clause needs market evidence or explicit terminal decision the company can't produce alone. Includes last write-refusal from directive-audit.log and last analyst promotion block. Never edits/clears directive, only reports. State file prevents re-notify within repeat-hours.

## Related

- uses [[directive-writer]] — Reads the directive and its audit log produced by directive_writer.
- uses [[telegram-notify]] — Sends staleness alerts via the shared Telegram script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
