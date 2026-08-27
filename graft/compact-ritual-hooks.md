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
    hash: 06d11935c31a1f1517fde00f600844f4bb48f1c1df968c063ab6cf3007458a81
  - path: scripts/compact-resume-lint.py
    hash: e8e8ee947a10358614b0125b2d236f26238308fff1b686565581748cf19122d3
  - path: scripts/context-watch.py
    hash: e9aa872c3ee33e6f175760da5b09d5cddda1ffdab5ac78c667547e492910bf96
sources_digest: 19a2a8b04acd80d73143d2cc1f5e5c9891f272b1685785df73160ccb605eaae3
links:
  - to: loop-driver
    relation: uses
    description: >-
      compact-report.py queries the cockpit state file and auto-loop log over
      SSH.
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
    at: 'scripts/compact-report.py:L66-L112'
  - symbol: grab
    kind: function
    at: 'scripts/compact-report.py:L88-L90'
  - symbol: main
    kind: function
    at: 'scripts/compact-report.py:L115-L124'
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

A family of Claude Code hooks that make the compact ritual measurable and safe: a preflight that counts open items at risk, a report that measures repo↔prod sync and loop health over SSH, a resume linter enforcing the foreign-reader test, a postcheck canary verifying the summary carries anchor sections, and a context-watch monitor that emits compact directives at 60% fullness. All are fail-open (never block the compact) and stdlib-only.

## Related

- uses [[loop-driver]] — compact-report.py queries the cockpit state file and auto-loop log over SSH.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
