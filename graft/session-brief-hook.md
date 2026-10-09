---
name: Session Brief Hook
slug: session-brief-hook
type: file
sources:
  - path: scripts/session-brief.py
    hash: f71655446ca0f9824d90922f64f2bbb113d24b5fc01df2dd8ff3fdfa99827dae
  - path: tests/test_compact_ritual_hardening.sh
    hash: 2d94865ee02e9d01b5770928d95abef8e3f9157576dc40326fb74e8a164408f9
sources_digest: 537884ec263537e7af22554f87aa4eab48031fb24ee2c82efc337741dcc5ca8a
links:
  - to: compact-ritual-path-resolution
    relation: uses
    description: Uses compact_yol.yol() to resolve resume/preflight paths
generator:
  version: 1
covers:
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L24-L28'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L31-L78'
---
<!-- context:generated:start -->
## Summary

A SessionStart hook injecting a measured, real-time session brief into agent context at startup/resume/compact. Gathers git state, checks resume file age via compact_yol, optionally runs .claude/brief-extra.sh, and reads a fresh preflight file to surface open ⚠ items for verification rather than blind adoption. Enforces the rule that the brief never blocks the session (8s timeout, silently empty on failure), and deliberately does not inject resume content — only its path and freshness.

## Related

- uses [[compact-ritual-path-resolution]] — Uses compact_yol.yol() to resolve resume/preflight paths
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
