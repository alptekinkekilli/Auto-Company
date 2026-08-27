# scripts/graft-auto-refresh.py · [[fail-open-vs-fail-closed-operational-philosophy]]

SessionStart hook that measures graft card freshness from git and, only when both thresholds are crossed, launches the paid deep build detached while always exiting 0.

- _repo_root · function · L42-L54 — Resolves the git repository root containing this script, returning None on any failure.
- _git · function · L57-L68 — Runs a git command in the repo and returns trimmed stdout, or None on error.
- _lock_alive · function · L71-L81 — Returns the pid from the lock file if that process is still alive, else None for missing/stale locks.
- _emit · function · L84-L94 — Prints the one-line status, best-effort writes freshness.json for the cockpit, and exits 0.
- main · function · L97-L187 — Computes graft freshness from git and, when the double threshold is crossed and no recent launch happened, launches the deep build detached in the background.
- status · function · L122-L132 — Builds the freshness status dict reported to stdout and the cockpit JSON.
- fmt · function · L134-L137 — Formats the behind/age pair as a compact 'Xc/Ys' string for the one-line output.
