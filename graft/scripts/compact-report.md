# scripts/compact-report.py · [[compact-ritual-hooks]]

PreCompact hook that prints a single operational digest (repo↔prod sync, OPREQ, directives, holds, loop health/cost) measured at the moment, complementing rather than repeating the compact security preflight.

- sh · function · L30-L35 — Runs a subprocess with a timeout and returns its trimmed stdout, returning an empty string on any failure so callers fail open.
- repo_root · function · L38-L40 — Resolves the repository root as the parent of the script's own directory.
- line_repo · function · L43-L51 — Appends a repo line showing the latest commit and whether any commits are unpushed to origin/main, flagging unpushed work with a warning.
- block_prod · function · L54-L63 — Delegates prod drift/hold/cockpit/directive/opreq measurement to the single source of truth .claude/brief-extra.sh (DRY), appending its output if executable.
- block_loop · function · L66-L112 — Performs one ssh round-trip to read the cockpit State File plus the latest auto-loop telemetry/cycle line and process liveness, appending a measured loop status line with a warning on errors or dead process.
- grab · function · L88-L90 — Extracts a single key=value field from the cockpit State File raw text, returning '?' when absent.
- main · function · L115-L124 — Assembles the digest header and repo/prod/loop blocks and prints them, always returning 0 so the compact is never blocked.
