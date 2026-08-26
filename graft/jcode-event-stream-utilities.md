---
name: jcode event-stream utilities
slug: jcode-event-stream-utilities
type: system
sources:
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
sources_digest: abdd4bc39eccdd8b14ff239eda058e6a67a4db17e25b504250ef6bd24972f74a
links:
  - to: jcode-mcp-boot-gate
    relation: uses
    description: >-
      tool-usage-audit and context7-check parse the same cycle-ndjson event
      format that the boot probe's StdioClient produces.
  - to: operator-escalation-gate
    relation: uses
    description: >-
      turn-audit's summary_line feeds the loop's per-cycle verdicts that
      operator_request_notify and bloat-trend consume.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/jcode-final-text.py:L30-L48'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-final-text.py:L51-L61'
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
  - symbol: calls_from_ndjson
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L43-L65'
  - symbol: categorize
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L68-L121'
  - symbol: main
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L124-L251'
  - symbol: dump
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L177-L190'
  - symbol: ts_of
    kind: function
    at: 'scripts/ops/turn-audit.py:L74-L78'
  - symbol: scan
    kind: function
    at: 'scripts/ops/turn-audit.py:L81-L112'
  - symbol: floor_usd
    kind: function
    at: 'scripts/ops/turn-audit.py:L115-L118'
  - symbol: summary_line
    kind: function
    at: 'scripts/ops/turn-audit.py:L121-L139'
  - symbol: main
    kind: function
    at: 'scripts/ops/turn-audit.py:L142-L155'
---
<!-- context:generated:start -->
## Summary

CLI helpers that read jcode's NDJSON event streams and daily logs to extract content and measure turn economics. They exist because jcode's own surfaces are unreliable: done.text truncates on tool-using runs, and command text is redacted so wait time must be proxied. All are stdlib-only, tolerate malformed lines via errors='replace', and exit non-zero on empty/error rather than crashing callers.

## Related

- uses [[jcode-mcp-boot-gate]] — tool-usage-audit and context7-check parse the same cycle-ndjson event format that the boot probe's StdioClient produces.
- uses [[operator-escalation-gate]] — turn-audit's summary_line feeds the loop's per-cycle verdicts that operator_request_notify and bloat-trend consume.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
