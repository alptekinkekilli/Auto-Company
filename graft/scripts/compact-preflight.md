# scripts/compact-preflight.py · [[compact-ritual-directive-integrity]] [[compact-ritual-hooks]]

Pre-compact hook that measures what would be lost in a compact and writes a report to /tmp for the post-compact session-brief to carry forward.

- sh · function · L24-L28 — Runs a shell command safely, returning its trimmed stdout or empty string on any failure/timeout.
- repo_report · function · L31-L48 — Inspects a git repo and counts open risks (unpushed commits, uncommitted changes, stashes) to flag what a compact could lose.
- main · function · L51-L80 — Aggregates risk across all roots plus optional project-specific checks and emits the preflight report to stdout and /tmp.
