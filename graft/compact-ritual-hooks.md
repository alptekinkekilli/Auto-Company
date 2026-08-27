---
name: Compact Ritual Hooks
slug: compact-ritual-hooks
type: system
sources:
  - path: scripts/compact-postcheck.py
    hash: 936578b4cf3b3bc9cca8769a142a20956d097aa08db4e84c963f1329c075857c
  - path: scripts/compact-preflight.py
    hash: e05718ceddc1954b8cefcea9ad00d143d0adb92d0d5547b55fe3916e5fbdb0b3
  - path: scripts/compact-report.py
    hash: d975b7144ba823824949e7a5518cf6381789605d40b521c1538f01ac9cb36c36
  - path: scripts/compact-resume-lint.py
    hash: e8e8ee947a10358614b0125b2d236f26238308fff1b686565581748cf19122d3
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: af7aabd2760269be5235f375db1044f09da3b09fedcd540e6bac3ad912985925
links:
  - to: loop-driver
    relation: uses
    description: >-
      compact-report.py SSHes to the powerupp-ts host to read the cockpit state
      file and tail telemetry.
generator:
  version: 1
covers:
  - symbol: main
    kind: function
    at: 'scripts/compact-postcheck.py:L34-L74'
  - symbol: sh
    kind: function
    at: 'scripts/compact-preflight.py:L24-L28'
  - symbol: repo_report
    kind: function
    at: 'scripts/compact-preflight.py:L31-L48'
  - symbol: main
    kind: function
    at: 'scripts/compact-preflight.py:L51-L80'
  - symbol: sh
    kind: function
    at: 'scripts/compact-report.py:L30-L35'
  - symbol: repo_root
    kind: function
    at: 'scripts/compact-report.py:L38-L40'
  - symbol: line_repo
    kind: function
    at: 'scripts/compact-report.py:L43-L51'
  - symbol: block_prod
    kind: function
    at: 'scripts/compact-report.py:L54-L63'
  - symbol: block_loop
    kind: function
    at: 'scripts/compact-report.py:L66-L146'
  - symbol: grab
    kind: function
    at: 'scripts/compact-report.py:L93-L95'
  - symbol: main
    kind: function
    at: 'scripts/compact-report.py:L149-L158'
  - symbol: main
    kind: function
    at: 'scripts/compact-resume-lint.py:L39-L71'
  - symbol: kullanim
    kind: function
    at: 'scripts/context-watch.py:L33-L50'
  - symbol: main
    kind: function
    at: 'scripts/context-watch.py:L53-L102'
---
<!-- context:generated:start -->
## Summary

A family of Claude Code hook scripts that make the context-compaction ritual measurable and safe: a preflight that counts open items that would be lost, a report that prints a live operational digest (fail-open, never blocks), a resume linter that enforces the 'foreign-reader test' by banning stale numeric claims, and a postcheck that verifies the compact summary carries the key anchor sections. All are fail-open and stdlib-only; the anchor list is deliberately kept in sync between the linter and postcheck.

## Related

- uses [[loop-driver]] — compact-report.py SSHes to the powerupp-ts host to read the cockpit state file and tail telemetry.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
