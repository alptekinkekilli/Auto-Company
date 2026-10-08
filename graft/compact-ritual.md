---
name: Compact Ritual
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
  - path: tests/test_compact_anchor_sync.py
    hash: 1f6ccedb49c760b6902820e32ca23f00f80927518fff9288ab1273aca4711378
  - path: tests/test_compact_ritual_hardening.sh
    hash: 2d94865ee02e9d01b5770928d95abef8e3f9157576dc40326fb74e8a164408f9
  - path: tests/test_compact_yol.py
    hash: 707405adc7816737d22c7079fe2e3484cb6959a80f4b4323acb76f44d4074e49
sources_digest: 6b3a535d4cd70b2cb1cc9c7e020b4c3d40e781ce37ab67eef2af1eff5ecfa371
links:
  - to: auto-loop-harness
    relation: uses
    description: >-
      session-brief.py is a SessionStart hook that injects a measured session
      brief at startup/resume/compact, reading the resume path and freshness
      from compact_yol.
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

The context-compaction ritual: preflight, resume-lint, postcheck, and path resolution. compact-preflight.py treats a resume as stale not only by mtime but also by running compact-resume-lint.py (so a fresh but lint-failing resume is flagged); compact-postcheck.py computes missing anchors and writes a JSON line to the history log; compact_yol.py derives ritual file paths from repository names to prevent cross-project collisions in shared /tmp paths, degrading gracefully to directory-name fallbacks on git timeouts. Core anchor strings (İLK İŞ, KARAR, DOĞRULANMAMIŞ, BEKLEYEN, İZLEYİCİ) must stay identical across the lint script, postcheck, the resume template, and the hardening test fixture — a hardcoded BEKLENEN tuple makes any intentional change explicit for reviewers.

## Related

- uses [[auto-loop-harness]] — session-brief.py is a SessionStart hook that injects a measured session brief at startup/resume/compact, reading the resume path and freshness from compact_yol.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
