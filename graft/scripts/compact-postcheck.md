# scripts/compact-postcheck.py · [[compact-ritual-directive-integrity]] [[compact-ritual-hooks]]

Post-compact audit hook that records whether the real compact_summary carried the required anchors, leaving a durable trace and a canary warning without blocking.

- main · function · L34-L74 — Reads the hook payload, checks which required anchors survived in compact_summary, appends an audit line to the log, and prints a canary warning when anchors are missing.
