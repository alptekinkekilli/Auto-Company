# scripts/ops/turn-audit.py · [[jcode-event-stream-utilities]] [[threshold-pinning-against-drift]] [[turn-audit-policy-engine]]

Turn-level waste accounting classifier over jcode's daily log, reporting per-session turn count, context growth, cache traffic, priced floor, tool census, wait-share, and a risk-calibrated verdict (ok/CHATTY/BLOATED).

- ts_of · function · L74-L78 — Parses a log line's bracketed timestamp into a float epoch seconds for duration/gap math.
- scan · function · L81-L112 — Aggregates per-session turn counts, cache tokens, tool wall times, and message maxima from the daily log lines.
- floor_usd · function · L115-L118 — Computes a priced cost floor from cache-write/read token counts at sonnet-5 1h-cache tariffs, deliberately understating the bill since in/out tokens are redacted.
- summary_line · function · L121-L139 — Builds the machine-readable audit line, computing duration, fast-gap count, tool wall share, and the risk-anchored verdict from turn/duration/cost thresholds.
- main · function · L142-L155 — Entry point that scans the log and prints either one summary line for the newest session (post-cycle hook) or all sessions with a tool census.
