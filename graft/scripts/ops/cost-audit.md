# scripts/ops/cost-audit.py · [[cost-budget-calibration]]

Deterministic daily cost audit that reads on-disk logs and writes memories/cost-audit.md so the Opportunity Analyst interprets measured numbers instead of computing them.

- utc_day · function · L42-L43 — Converts an epoch timestamp to a UTC date string for bucketing ledger rows by day.
- read_ledger · function · L46-L67 — Parses the spend-total ledger into per-day cycle rows, filtering to the last N days and counting malformed lines.
- read_loop_log · function · L70-L111 — Extracts today's cycle cost/provenance, timeout, and turn-audit facts from the auto-loop log, tagging each cycle as estimated/hinted.
- read_jcode_log · function · L114-L131 — Parses the jcode session log for prompt-prefix token counts, tool-list lock sizes, and per-tool call tallies.
- read_tool_inventory · function · L134-L141 — Loads the MCP schema cache into a map of server name to advertised tool names.
- fmt_money · function · L144-L145 — Formats a float as a two-decimal USD currency string.
- build_report · function · L148-L303 — Assembles the full cost-audit markdown report from ledger, loop, jcode, and tool-inventory data, reporting on the previous completed UTC day and routing findings as company-fixable vs infra.
- main · function · L306-L324 — Parses CLI args, builds the report, and atomically writes it to the output file via a temp file and os.replace.
