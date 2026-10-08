---
name: Turn economics auditing
slug: turn-economics-auditing
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
  - to: airtable-read-write-guards
    relation: uses
    description: >-
      web-research-cost.py found Airtable dumps to be the largest context
      source, motivating the read-scoping wrapper.
  - to: work-window-bloat-brakes
    relation: produces
    description: turn-audit.py emits the BLOATED verdict that turn-bloat-brake.py tracks.
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

Per-cycle cost and turn-economics measurement: turn-audit.py parses jcode's daily log to measure turn count, context growth, cache traffic, a priced cost floor (sonnet-5 cache tariff, deliberately understating because in/out tokens are redacted), and tool census; web-research-cost.py corrects the naive 'a fetch costs once' assumption by scoring residual cost as output_tokens × turns_after × cache-read rate across all tools (not just web ones, since Airtable dumps were the largest hidden source); tool-usage-audit.py maintains a durable per-cycle ledger for the cockpit's Tool Analytics panel. Verdict thresholds were recalibrated against 34 measured cycles.

## Related

- uses [[airtable-read-write-guards]] — web-research-cost.py found Airtable dumps to be the largest context source, motivating the read-scoping wrapper.
- produces [[work-window-bloat-brakes]] — turn-audit.py emits the BLOATED verdict that turn-bloat-brake.py tracks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
