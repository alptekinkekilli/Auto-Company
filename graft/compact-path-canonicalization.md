---
name: Compact Path Canonicalization
slug: compact-path-canonicalization
type: concept
sources:
  - path: scripts/compact_yol.py
    hash: 617adabc76e0edaa59787115e1c95e883fa607510c8483a701a97df4539f17da
sources_digest: 05ce3c381678337934f81ea346092efb546335111ae44cc829dcdd403afd016e
links:
  - to: compact-ritual-hooks
    relation: part_of
    description: Provides canonical paths used by all compact hooks.
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
---
<!-- context:generated:start -->
## Summary

Repo-specific temporary file paths for the compact ritual, replacing shared /tmp paths that caused cross-project state collisions. Derives a stable repo name from git metadata (worktrees, submodules, non-git fallbacks), sanitizes to [a-z0-9-], and honors COMPACT_* env overrides. Never raises (hooks fail open), no fallback to legacy shared paths, repo root derived from file location not CWD.

## Related

- part of [[compact-ritual-hooks]] — Provides canonical paths used by all compact hooks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
