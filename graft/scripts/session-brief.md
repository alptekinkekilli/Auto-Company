# scripts/session-brief.py · [[claude-code-hooks]]

SessionStart hook that injects a measured, non-stale session briefing into the context, never blocking the session.

- sh · function · L19-L23 — Runs a shell command safely, returning stripped stdout or empty string on any failure/timeout.
- main · function · L26-L63 — Builds the briefing by measuring git state, optional extra script output, and fresh precompact warnings, then prints it.
