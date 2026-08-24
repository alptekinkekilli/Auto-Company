---
name: jcode event-stream utilities
slug: jcode-event-stream-utilities
type: system
sources:
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
  - path: scripts/ops/tool-usage-audit.py
    hash: 1e21a81523cfbf8e4c6b9b1ee7782201c293b73feebe7494fd91494587ec9a4e
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
sources_digest: 4dfa17211fdde790194debd985d6de5069d111a03a4cc31361b0514971169261
links:
  - to: cost-budget-reporting
    relation: produces
    description: >-
      turn-audit verdict lines and tool-usage ledger feed cost-audit and
      bloat-trend.
  - to: mcp-boot-config-generation
    relation: uses
    description: >-
      turn-audit and tool-usage-audit parse the same jcode log format that
      jcode-mcp-config/probe generate and verify.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/jcode-final-text.py:L30-L48'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-final-text.py:L51-L61'
  - symbol: calls_from_ndjson
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L43-L65'
  - symbol: categorize
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L68-L114'
  - symbol: main
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L117-L244'
  - symbol: dump
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L170-L183'
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

CLI tools that parse jcode's NDJSON event streams and logs to extract reliable signals: final assistant text (preferring concatenated text_delta over unreliable done.text), per-session turn economics, and tool-call census. All read with errors='replace' and tolerate malformed lines, and all deliberately prefer measured/derived facts over self-reported fields because jcode redacts tokens and truncates done.text on tool-using runs.

## Related

- produces [[cost-budget-reporting]] — turn-audit verdict lines and tool-usage ledger feed cost-audit and bloat-trend.
- uses [[mcp-boot-config-generation]] — turn-audit and tool-usage-audit parse the same jcode log format that jcode-mcp-config/probe generate and verify.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
