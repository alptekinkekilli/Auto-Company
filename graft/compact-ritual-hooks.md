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
sources_digest: d2deeac1293676cc298f20dece4303bda8fc4beb118ac862af9f1aa5e1ec1f7a
links:
  - to: context-watch
    relation: uses
    description: >-
      compact-preflight.py writes /tmp/compact-preflight.md for session-brief.py
      to read after compact; the hooks are triggered by the same compact ritual
      context-watch.py directs.
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
---
<!-- context:generated:start -->
## Summary

Set of Claude Code hooks that make the compact ritual measurable and safe: compact-preflight.py counts open items (unpushed commits, uncommitted changes, stashes) that would be lost; compact-report.py prints an operational digest (repo↔prod sync, OPREQ, directives, holds, pending external actions, loop health) via SSH to the powerupp-ts host; compact-resume-lint.py enforces the 'foreign-reader test' banning stale numeric claims (YASAK) and requiring template sections (ZORUNLU); compact-postcheck.py verifies the generated compact_summary carries the five mandatory anchors. All are fail-open (never block compact, always exit 0) and depend only on the Python standard library plus git/SSH CLIs.

## Related

- uses [[context-watch]] — compact-preflight.py writes /tmp/compact-preflight.md for session-brief.py to read after compact; the hooks are triggered by the same compact ritual context-watch.py directs.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
