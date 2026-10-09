---
name: Compact Ritual Path Resolution
slug: compact-ritual-path-resolution
type: file
sources:
  - path: scripts/compact_yol.py
    hash: 617adabc76e0edaa59787115e1c95e883fa607510c8483a701a97df4539f17da
  - path: tests/test_compact_yol.py
    hash: 707405adc7816737d22c7079fe2e3484cb6959a80f4b4323acb76f44d4074e49
sources_digest: e916153aa1881c244d4fa0d3f3377ed1d95468fb6a004f30dbd84b148c2b8b10
links:
  - to: session-brief-hook
    relation: implements
    description: Provides the path-resolution contract session-brief.py relies on
generator:
  version: 1
covers:
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

compact_yol.py derives ritual file paths (resume, preflight, marker, history) from repository names to prevent cross-project collisions in shared /tmp paths. Handles normal repos, linked worktrees (appending branch suffix), submodules, and non-git directories with graceful fallbacks; COMPACT_* env vars override defaults. Git timeouts or missing git binaries degrade to directory-name fallbacks without exceptions.

## Related

- implements [[session-brief-hook]] — Provides the path-resolution contract session-brief.py relies on
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
