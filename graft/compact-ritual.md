---
name: Compact Ritual
slug: compact-ritual
type: system
sources:
  - path: scripts/compact-postcheck.py
    hash: 936578b4cf3b3bc9cca8769a142a20956d097aa08db4e84c963f1329c075857c
  - path: scripts/compact-preflight.py
    hash: e05718ceddc1954b8cefcea9ad00d143d0adb92d0d5547b55fe3916e5fbdb0b3
  - path: scripts/compact-resume-lint.py
    hash: e8e8ee947a10358614b0125b2d236f26238308fff1b686565581748cf19122d3
  - path: tests/test_compact_anchor_sync.py
    hash: 1f6ccedb49c760b6902820e32ca23f00f80927518fff9288ab1273aca4711378
  - path: tests/test_compact_ritual_hardening.sh
    hash: de188f563de5c279fd57ce9442d97611df89cf84112ae99d4c6021ad45635051
sources_digest: a197cb7f52298831dc305a1eb2c78fa466f5497a161e0089f9616dba6381229c
links:
  - to: auto-loop-core
    relation: uses
    description: >-
      Compact runs as part of the loop lifecycle; session-brief surfaces
      /tmp/compact-preflight.md open items.
  - to: context-watch
    relation: uses
    description: >-
      context-watch.py emits the compact-ritual directive at 60% context
      fullness, triggering this ritual.
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
  - symbol: _load
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L41-L45'
  - symbol: check
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L48-L53'
  - symbol: test_hepsi_gecti
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L88-L89'
---
<!-- context:generated:start -->
## Summary

The measurable compact ritual: a preflight that counts open items that would be lost, a resume linter enforcing the foreign-reader test (banning stale numeric claims while allowing commit SHAs/task IDs as stable anchors), and a postcheck that verifies the compact_summary carries the five mandatory anchor sections. All are fail-open canaries that never block compaction, and the anchor list is kept in sync across the linter and postcheck.

## Related

- uses [[auto-loop-core]] — Compact runs as part of the loop lifecycle; session-brief surfaces /tmp/compact-preflight.md open items.
- uses [[context-watch]] — context-watch.py emits the compact-ritual directive at 60% context fullness, triggering this ritual.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
