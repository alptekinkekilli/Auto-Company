---
name: evidence extraction & compliance
slug: evidence-extraction-compliance
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/ops/extract-axis-evidence.py
    hash: 3f3d55a2a285cd52ab3b0d286b1f908b877283bfde69b03e442d10758080f567
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
sources_digest: d4d24215efb730ede683f8f3e9e3f20aaeecca474b150c1b466e269e0c7ab1ce
links:
  - to: jcode-event-stream-utilities
    relation: uses
    description: >-
      context7-check.py reads the same cycle-ndjson event format as
      tool-usage-audit.
generator:
  version: 1
covers:
  - symbol: externals
    kind: function
    at: 'scripts/ops/context7-check.py:L59-L75'
  - symbol: scan
    kind: function
    at: 'scripts/ops/context7-check.py:L78-L108'
  - symbol: walk_calls
    kind: function
    at: 'scripts/ops/context7-check.py:L111-L122'
  - symbol: verdict
    kind: function
    at: 'scripts/ops/context7-check.py:L125-L138'
  - symbol: main
    kind: function
    at: 'scripts/ops/context7-check.py:L141-L170'
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
---
<!-- context:generated:start -->
## Summary

Strict, fail-closed extraction and compliance checkers. extract-axis-evidence.py pulls screened axis headings/bodies from discovery-scan markdown, failing on any unreadable file, empty body, or count mismatch so output never silently omits evidence. context7-check.py detects whether an agent wrote code importing an external library without first calling Context7, deliberately avoiding prefiltering on exact JSON strings (which caused silent false negatives) and reporting to the LOG rather than blocking. idle-skip-note.py records model-free idle-skip events into consensus.md as one auditable line per day.

## Related

- uses [[jcode-event-stream-utilities]] — context7-check.py reads the same cycle-ndjson event format as tool-usage-audit.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
