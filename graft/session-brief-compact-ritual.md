---
name: Session Brief & Compact Ritual
slug: session-brief-compact-ritual
type: system
sources:
  - path: scripts/session-brief.py
    hash: f71655446ca0f9824d90922f64f2bbb113d24b5fc01df2dd8ff3fdfa99827dae
  - path: tests/test_compact_anchor_sync.py
    hash: 1f6ccedb49c760b6902820e32ca23f00f80927518fff9288ab1273aca4711378
  - path: tests/test_compact_ritual_hardening.sh
    hash: 2d94865ee02e9d01b5770928d95abef8e3f9157576dc40326fb74e8a164408f9
  - path: tests/test_compact_yol.py
    hash: 707405adc7816737d22c7079fe2e3484cb6959a80f4b4323acb76f44d4074e49
sources_digest: 3c62da0ecfdd1d5ea8e18f21665f42588364eb13f72704b2fba22d19992c35a0
links:
  - to: auto-loop-harness
    relation: uses
    description: >-
      session-brief runs as a SessionStart hook; compact ritual runs at compact
      events.
generator:
  version: 1
covers:
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L24-L28'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L31-L78'
  - symbol: _load
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L41-L45'
  - symbol: check
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L48-L53'
  - symbol: test_hepsi_gecti
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L88-L89'
  - symbol: check
    kind: function
    at: 'tests/test_compact_yol.py:L31-L36'
  - symbol: _load
    kind: function
    at: 'tests/test_compact_yol.py:L39-L43'
  - symbol: git
    kind: function
    at: 'tests/test_compact_yol.py:L46-L49'
  - symbol: yeni_repo
    kind: function
    at: 'tests/test_compact_yol.py:L52-L59'
  - symbol: temiz_env
    kind: function
    at: 'tests/test_compact_yol.py:L62-L63'
  - symbol: zaman_asimi
    kind: function
    at: 'tests/test_compact_yol.py:L120-L122'
  - symbol: git_yok
    kind: function
    at: 'tests/test_compact_yol.py:L124-L125'
  - symbol: test_hepsi_gecti
    kind: function
    at: 'tests/test_compact_yol.py:L163-L164'
---
<!-- context:generated:start -->
## Summary

The session-start and compact-resume machinery: session-brief.py injects a measured real-time brief (git state, resume freshness, optional brief-extra.sh) at startup/resume/compact, never blocking the session and never injecting resume content — only its path and freshness. The compact ritual (compact_yol.py path derivation, compact-resume-lint.py, compact-postcheck.py, compact-preflight.py) enforces that core anchor strings stay identical across four locations and that a fresh-but-lint-failing resume is flagged stale.

## Related

- uses [[auto-loop-harness]] — session-brief runs as a SessionStart hook; compact ritual runs at compact events.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
