---
name: Tool Usage and Turn Ledgers
slug: tool-usage-and-turn-ledgers
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
sources_digest: d7be2b5067a49c007c7c9c1420a8e39b4d682342d8a075c2e519b580a6b0a037
links:
  - to: cycle-cost-and-turn-economics
    relation: produces
    description: Feeds the tool census and turn metrics used by cost analysis
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
---
<!-- context:generated:start -->
## Summary

Durable per-cycle ledgers that power the cockpit's analytics panels: tool-usage-audit.py appends one JSON line per cycle to logs/tool-usage-history.ndjson (deduping on filename+size+mtime, not name alone, because the cycle counter restarts on container restart), and turn-audit.py parses jcode's daily log to measure turn economics. Both use only the standard library, always exit 0, and backfill retained-but-unprocessed data on the next run.

## Related

- produces [[cycle-cost-and-turn-economics]] — Feeds the tool census and turn metrics used by cost analysis
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
