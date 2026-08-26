---
name: Context & Compact Hooks
slug: context-compact-hooks
type: system
sources:
  - path: scripts/compact-preflight.py
    hash: e05718ceddc1954b8cefcea9ad00d143d0adb92d0d5547b55fe3916e5fbdb0b3
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: 36e2492447e7ec5e61486860d79762b85b2182f8f99c57081cc7b63ff3b1804c
links:
  - to: auto-loop-daemon
    relation: part_of
    description: Hooks that run inside agent sessions orchestrated by auto-loop.sh.
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

Claude Code hook scripts that monitor context-window fullness and make the compact ritual measurable. context-watch.py reads the transcript's usage field, sums input/cache tokens, auto-escalates the window size through tiers up to 2M, and emits a warning at 50% or a compact directive at 60% (nested inside hookSpecificOutput or silently ignored), persisting per-session state so each threshold fires once and re-arms below 40%. compact-preflight.py counts open items (unpushed commits, uncommitted changes, stashes) that would be lost on compaction, runs an optional .claude/preflight-extra.sh, and always exits 0 so it never blocks the compact.

## Related

- part of [[auto-loop-daemon]] — Hooks that run inside agent sessions orchestrated by auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
