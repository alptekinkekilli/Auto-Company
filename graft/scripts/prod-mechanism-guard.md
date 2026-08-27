# scripts/prod-mechanism-guard.py · [[prod-mechanism-guard]] [[prod-mechanism-guard-session-brief]]

PreToolUse tripwire that mechanically blocks unplanned edits to protected prod surfaces unless a fresh operator-approval marker exists, and verifies the guard's protected list stays in sync with CLAUDE.md's rule section.

- is_protected · function · L48-L51 — Decides whether a given path is a protected prod surface by matching against configured suffixes and basenames.
- check_sync · function · L54-L80 — Detects scope drift by parsing backtick tokens from CLAUDE.md's rule section and failing if any named surface is not covered by the protected lists.
- main · function · L83-L125 — Enforces the prod-change rule at edit time: no-ops in container, parses the hook payload, and blocks writes to protected files unless a non-stale approval marker exists.
