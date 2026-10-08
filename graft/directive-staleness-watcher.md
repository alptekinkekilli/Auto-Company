---
name: Directive staleness watcher
slug: directive-staleness-watcher
type: system
sources:
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
sources_digest: 2da49c6c22e53f06775d58264310e950958b2bae6d54fa684cf37a2c50d95a4d
links:
  - to: directive-writer-human-directive-md
    relation: depends_on
    description: >-
      Relies on the writer's audit log wording and the directive's exact
      Status/Updated format.
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

Alerts when the human directive stays PENDING beyond a threshold, because its completion clause can only be satisfied by market evidence or an explicit terminal decision the company cannot produce alone. Persists last-notified timestamp to avoid spamming a 15-minute cron, never edits the directive, and swallows notification failures so the watcher never crashes.

## Related

- depends on [[directive-writer-human-directive-md]] — Relies on the writer's audit log wording and the directive's exact Status/Updated format.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
