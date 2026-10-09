---
name: Compact Ritual Hardening
slug: compact-ritual-hardening
type: system
sources:
  - path: tests/test_compact_anchor_sync.py
    hash: 1f6ccedb49c760b6902820e32ca23f00f80927518fff9288ab1273aca4711378
  - path: tests/test_compact_ritual_hardening.sh
    hash: 2d94865ee02e9d01b5770928d95abef8e3f9157576dc40326fb74e8a164408f9
sources_digest: f1a266b755b5afa6e87c8dcf1bc900f2cae8a67d610d5091cfb85be4e89497cb
links:
  - to: compact-ritual-path-resolution
    relation: uses
    description: Path resolution isolated from real repo files via compact_yol.py
generator:
  version: 1
covers:
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

The compact ritual's integrity checks: compact-preflight.py treats a resume as stale not only by mtime but also by running compact-resume-lint.py (so a fresh but lint-failing resume is flagged), compact-postcheck.py computes missing anchors and writes a JSON line to the history log, and a test enforces that the core anchor strings ('İLK İŞ', 'KARAR', 'DOĞRULANMAMIŞ', 'BEKLEYEN', 'İZLEYİCİ') stay identical across four locations. A hardcoded BEKLENEN tuple acts as a deliberate anchor making any intentional anchor change explicit in diffs.

## Related

- uses [[compact-ritual-path-resolution]] — Path resolution isolated from real repo files via compact_yol.py
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
