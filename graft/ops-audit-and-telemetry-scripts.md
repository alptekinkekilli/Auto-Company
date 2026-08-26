---
name: ops-audit-and-telemetry-scripts
slug: ops-audit-and-telemetry-scripts
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
sources_digest: 05a5a8135b793a7ae3595f1faa0f4445138043d5ad416b12ef019fd435434902
links:
  - to: auto-loop-core
    relation: produces
    description: >-
      The cycle ndjson files these scripts consume are written by the auto-loop
      engine's jcode harness.
  - to: cycle-ndjson-log-format
    relation: uses
    description: >-
      All three parse the jcode event stream (tool_start, tool_input deltas,
      tokens, tool_done) from logs/cycle-ndjson; a change to that format breaks
      their parsers.
generator:
  version: 1
covers:
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
  - symbol: is_web
    kind: function
    at: 'scripts/ops/web-research-cost.py:L43-L44'
  - symbol: analyse
    kind: function
    at: 'scripts/ops/web-research-cost.py:L47-L76'
  - symbol: main
    kind: function
    at: 'scripts/ops/web-research-cost.py:L79-L161'
---
<!-- context:generated:start -->
## Summary

A family of standalone stdlib-only Python CLI tools that parse jcode/cycle NDJSON logs and produce durable ledgers, cost models, and audits for the cockpit. They share conventions: read from logs/cycle-ndjson, append to logs/*.ndjson, dedup via state files keyed on filename+size+mtime, always exit 0, and backfill unprocessed files on next run.

## Related

- produces [[auto-loop-core]] — The cycle ndjson files these scripts consume are written by the auto-loop engine's jcode harness.
- uses [[cycle-ndjson-log-format]] — All three parse the jcode event stream (tool_start, tool_input deltas, tokens, tool_done) from logs/cycle-ndjson; a change to that format breaks their parsers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
