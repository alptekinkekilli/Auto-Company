---
name: ops_archive_and_state
slug: ops-archive-and-state
type: system
sources:
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: tests/test_registry_archive.sh
    hash: 4ca1be679dfb4867f1e05625b59c587e0a40e525f53c35404d535f93017e5c76
  - path: tests/test_state_snapshot.sh
    hash: 44428d24f7cb21d69c1f03477dd4b07ce31b98c94879131f75d58d146aa08729
sources_digest: ff698ae6660b9f7c63784138d5516014811ee7dace0de30e45ed93432d210966
links:
  - to: operator-request-notify
    relation: uses
    description: >-
      state-snapshot.py reads the same human-directive.md and
      operator-requests.md files the notify script resolves.
generator:
  version: 1
covers:
  - symbol: die
    kind: function
    at: 'scripts/ops/registry-archive.py:L55-L57'
  - symbol: sha
    kind: function
    at: 'scripts/ops/registry-archive.py:L60-L61'
  - symbol: heading_line_starts
    kind: function
    at: 'scripts/ops/registry-archive.py:L64-L65'
  - symbol: protected_span
    kind: function
    at: 'scripts/ops/registry-archive.py:L68-L80'
  - symbol: plan_note_chunks
    kind: function
    at: 'scripts/ops/registry-archive.py:L83-L105'
  - symbol: plan_section_chunks
    kind: function
    at: 'scripts/ops/registry-archive.py:L108-L140'
  - symbol: interleave
    kind: function
    at: 'scripts/ops/registry-archive.py:L143-L149'
  - symbol: main
    kind: function
    at: 'scripts/ops/registry-archive.py:L152-L340'
  - symbol: month_of
    kind: function
    at: 'scripts/ops/registry-archive.py:L250-L251'
  - symbol: file_sha16
    kind: function
    at: 'scripts/ops/state-snapshot.py:L54-L61'
  - symbol: directive_state
    kind: function
    at: 'scripts/ops/state-snapshot.py:L64-L72'
  - symbol: opreq_open
    kind: function
    at: 'scripts/ops/state-snapshot.py:L75-L87'
  - symbol: wowcar_sources
    kind: function
    at: 'scripts/ops/state-snapshot.py:L90-L104'
  - symbol: main
    kind: function
    at: 'scripts/ops/state-snapshot.py:L107-L166'
---
<!-- context:generated:start -->
## Summary

scripts/ops maintenance tools for registry and state management. registry-archive.py archives stale dated sections from a candidate registry markdown into a monthly archive file, preserving a protected live span (## Selected through ## Exhausted patterns / lessons) byte-identical, never moving frozen-pattern sections inside that region, with dry-run/apply/check modes and idempotence. state-snapshot.py parses directive status/sha16 and OPREQ open counts into DELTA change-detection output, excluding errored fields from the next DELTA and printing an error (but exiting 0) on a missing ledger.

## Related

- uses [[operator-request-notify]] — state-snapshot.py reads the same human-directive.md and operator-requests.md files the notify script resolves.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
