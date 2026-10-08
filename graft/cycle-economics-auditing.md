---
name: Cycle Economics Auditing
slug: cycle-economics-auditing
type: system
sources:
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
  - path: tests/test_cost_audit_tool_surface.py
    hash: 801b92c715ca95cef9c34ab863f87fa443c8abcc65ba03237a934f5aed78121a
sources_digest: dc0ede8cd85dc3a4d948090fae8035c8c11487aa7cb52e660d950c18c109de0d
links:
  - to: cycle-escalation-brakes
    relation: produces
    description: >-
      turn-audit.py's verdicts (BLOATED etc.) feed turn-bloat-brake.py's streak
      tracking; the cost floor and tool census inform the budget gates.
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
  - symbol: ok
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L24-L25'
  - symbol: 'no'
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L28-L31'
---
<!-- context:generated:start -->
## Summary

A set of per-cycle auditors that measure LLM turn economics, tool usage, and web-research cost from jcode NDJSON event streams and daily logs, feeding the cockpit's analytics panels and post-cycle hooks. turn-audit.py measures turn count, context growth, cache traffic, a priced cost floor, tool census, and wait-share (tool wall-time is a proxy for wait because command text is redacted). tool-usage-audit.py reassembles tool calls from the jcode event stream and categorizes them, deduping on filename+size+mtime (not name alone, because the cycle counter restarts on container restart). web-research-cost.py corrects the naive assumption that a fetch costs once: each tool result is re-read on every subsequent turn, so cost scales with output size times remaining turns, and it deliberately scores all tools because pre-filtering by category hid the largest context source (Airtable dumps).

## Related

- produces [[cycle-escalation-brakes]] — turn-audit.py's verdicts (BLOATED etc.) feed turn-bloat-brake.py's streak tracking; the cost floor and tool census inform the budget gates.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
