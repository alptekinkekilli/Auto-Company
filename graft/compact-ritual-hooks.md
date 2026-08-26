---
name: Compact Ritual Hooks
slug: compact-ritual-hooks
type: system
sources:
  - path: scripts/compact-postcheck.py
    hash: 936578b4cf3b3bc9cca8769a142a20956d097aa08db4e84c963f1329c075857c
  - path: scripts/compact-preflight.py
    hash: e05718ceddc1954b8cefcea9ad00d143d0adb92d0d5547b55fe3916e5fbdb0b3
  - path: scripts/compact-resume-lint.py
    hash: e8e8ee947a10358614b0125b2d236f26238308fff1b686565581748cf19122d3
sources_digest: 8a29be38a180ad8d9499a56cd3d111ad43039671f2ed2e59086a14253cad9064
links:
  - to: context-watch
    relation: uses
    description: >-
      context-watch.py emits the compact-ritual directive at 60% fullness that
      triggers these hooks.
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
  - symbol: main
    kind: function
    at: 'scripts/compact-resume-lint.py:L39-L71'
---
<!-- context:generated:start -->
## Summary

A set of Claude Code hook scripts that make the compact ritual measurable and safe. compact-preflight.py counts open items (unpushed commits, uncommitted changes, stashes) that would be lost, writing /tmp/compact-preflight.md for session-brief.py; compact-resume-lint.py enforces the 'foreign-reader test' banning stale numeric claims (dollar amounts, queue counts, budget assertions) while allowing commit SHAs/task IDs as stable anchors, and requires the template sections; compact-postcheck.py verifies the generated compact_summary carries the five mandatory anchors, framing missing anchors as a canary signal rather than proof of loss. All are fail-open (exit 0) so they never block the compact itself.

## Related

- uses [[context-watch]] — context-watch.py emits the compact-ritual directive at 60% fullness that triggers these hooks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
