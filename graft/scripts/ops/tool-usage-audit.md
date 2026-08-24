# scripts/ops/tool-usage-audit.py · [[jcode-event-stream-utilities]] [[tool-usage-audit]]

Durable per-cycle ledger of tool-consultation counts (ctx7/Airtable/Linear/Browser) appended from finished cycle ndjson, idempotent via a state file, so the cockpit's Tool Analytics panel can show multi-day usage.

- calls_from_ndjson · function · L43-L65 — Reassembles tool calls from jcode's event stream by pairing tool_start with streamed tool_input deltas, since tool_exec carries no input.
- categorize · function · L68-L114 — Classifies each reassembled call into usage categories by matching bash command substrings or MCP tool names, and tallies per-MCP-tool-name counts for denylist decisions.
- main · function · L117-L244 — Orchestrates the audit: handles --report/--names read-only modes, and otherwise appends one JSON row per newly-changed cycle ndjson to the durable ledger while tracking processed files by size+mtime.
- dump · function · L170-L183 — Prints a sorted per-tool-name and per-server breakdown for a given name-count source in the --names report.
