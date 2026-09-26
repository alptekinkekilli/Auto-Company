---
name: Compact ritual
slug: compact-ritual
type: system
sources:
  - path: scripts/compact_yol.py
    hash: 617adabc76e0edaa59787115e1c95e883fa607510c8483a701a97df4539f17da
  - path: scripts/compact-postcheck.py
    hash: 9584b13bce7ed4eba756912e4a2fbd65beaa2f46bf8cb0238b29d77574ca258f
  - path: scripts/compact-preflight.py
    hash: 879a08b82fae1518773088e60a44ea3e7e941736c9e7e46593201797bf951797
  - path: scripts/compact-resume-lint.py
    hash: 721ece8bebbdbef80a1b67bb8573a3083b213175e0bda2277a9c46b976c300e1
  - path: scripts/session-brief.py
    hash: f71655446ca0f9824d90922f64f2bbb113d24b5fc01df2dd8ff3fdfa99827dae
sources_digest: 8904b3b66b2a02bfb4a1c298774e4cbe51c53b421aa0c5ab81e9035faefa1c2e
links:
  - to: auto-loop-harness
    relation: uses
    description: >-
      The compact ritual runs as part of the loop lifecycle; session-brief.py is
      a SessionStart hook.
generator:
  version: 1
covers:
  - symbol: main
    kind: function
    at: 'scripts/compact-postcheck.py:L39-L79'
  - symbol: sh
    kind: function
    at: 'scripts/compact-preflight.py:L52-L56'
  - symbol: hook_payload
    kind: function
    at: 'scripts/compact-preflight.py:L59-L68'
  - symbol: resume_lint_gecer_mi
    kind: function
    at: 'scripts/compact-preflight.py:L71-L87'
  - symbol: resume_durumu
    kind: function
    at: 'scripts/compact-preflight.py:L90-L100'
  - symbol: repo_report
    kind: function
    at: 'scripts/compact-preflight.py:L103-L120'
  - symbol: main
    kind: function
    at: 'scripts/compact-preflight.py:L123-L193'
  - symbol: main
    kind: function
    at: 'scripts/compact-resume-lint.py:L45-L77'
  - symbol: temizle
    kind: function
    at: 'scripts/compact_yol.py:L57-L60'
  - symbol: _git
    kind: function
    at: 'scripts/compact_yol.py:L63-L69'
  - symbol: repo_adi
    kind: function
    at: 'scripts/compact_yol.py:L72-L89'
  - symbol: yol
    kind: function
    at: 'scripts/compact_yol.py:L92-L95'
  - symbol: main
    kind: function
    at: 'scripts/compact_yol.py:L98-L107'
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L24-L28'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L31-L78'
---
<!-- context:generated:start -->
## Summary

The context-compaction machinery: compact_yol.py derives ritual file paths from repository names to prevent cross-project collisions in shared /tmp paths; compact-preflight.py, compact-resume-lint.py, and compact-postcheck.py enforce that a resume is stale by mtime AND lint-passing, and that all anchors are present. session-brief.py is the SessionStart hook that injects a measured brief and never blocks the session.

## Related

- uses [[auto-loop-harness]] — The compact ritual runs as part of the loop lifecycle; session-brief.py is a SessionStart hook.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
