---
name: Context Monitoring Hooks
slug: context-monitoring-hooks
type: system
sources:
  - path: scripts/compact-preflight.py
    hash: e05718ceddc1954b8cefcea9ad00d143d0adb92d0d5547b55fe3916e5fbdb0b3
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: 36e2492447e7ec5e61486860d79762b85b2182f8f99c57081cc7b63ff3b1804c
links:
  - to: auto-loop
    relation: configures
    description: >-
      These hooks run inside agent sessions the loop spawns, guiding compaction
      behavior.
generator:
  version: 1
covers:
  - symbol: sh
    kind: function
    at: 'scripts/compact-preflight.py:L24-L28'
  - symbol: repo_report
    kind: function
    at: 'scripts/compact-preflight.py:L31-L48'
  - symbol: main
    kind: function
    at: 'scripts/compact-preflight.py:L51-L80'
  - symbol: kullanim
    kind: function
    at: 'scripts/context-watch.py:L33-L50'
  - symbol: main
    kind: function
    at: 'scripts/context-watch.py:L53-L102'
---
<!-- context:generated:start -->
## Summary

Claude Code hook scripts that make the compact ritual measurable and monitor context-window fullness. compact-preflight.py counts open items (unpushed commits, uncommitted changes, stashes) that would be lost on compaction, writing a report to /tmp/compact-preflight.md for session-brief.py and always exiting 0 so it never blocks the compact. context-watch.py reads the session transcript, sums input/cache tokens, and emits warnings at 50% and a compact directive at 60%, with per-session state so each threshold fires once and re-arms below 40%.

## Related

- configures [[auto-loop]] — These hooks run inside agent sessions the loop spawns, guiding compaction behavior.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
