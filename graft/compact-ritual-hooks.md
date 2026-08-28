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
    hash: acbd35a8779fa472cd8164183bcc13c79e716e9e05a51473b0cd2e1b5e2375d1
  - path: scripts/compact-resume-lint.py
    hash: e8e8ee947a10358614b0125b2d236f26238308fff1b686565581748cf19122d3
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: 3e1f7decf296003fe5b5c4e8235d5f7ca6726cf6b6d57abf44a9e917d93999f8
links:
  - to: auto-loop
    relation: uses
    description: >-
      compact-report reads loop state via SSH/docker exec and
      discretionary-spend.ndjson.
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
  - symbol: sh_input
    kind: function
    at: 'scripts/compact-report.py:L38-L43'
  - symbol: repo_root
    kind: function
    at: 'scripts/compact-report.py:L46-L48'
  - symbol: line_repo
    kind: function
    at: 'scripts/compact-report.py:L51-L59'
  - symbol: block_prod
    kind: function
    at: 'scripts/compact-report.py:L62-L71'
  - symbol: block_loop
    kind: function
    at: 'scripts/compact-report.py:L74-L145'
  - symbol: grab
    kind: function
    at: 'scripts/compact-report.py:L101-L103'
  - symbol: block_discretionary
    kind: function
    at: 'scripts/compact-report.py:L148-L199'
  - symbol: g
    kind: function
    at: 'scripts/compact-report.py:L186-L188'
  - symbol: main
    kind: function
    at: 'scripts/compact-report.py:L202-L212'
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

A family of Claude Code hook scripts that make the compact ritual measurable and safe: preflight counts open items that would be lost, resume-lint enforces the foreign-reader test on the resume file, report prints an operational digest, postcheck verifies the compact_summary carries key anchors, and context-watch monitors context-window fullness and emits a compact directive at 60%. All are fail-open and never block the compact itself.

## Related

- uses [[auto-loop]] — compact-report reads loop state via SSH/docker exec and discretionary-spend.ndjson.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
