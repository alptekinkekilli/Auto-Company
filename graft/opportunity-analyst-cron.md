---
name: Opportunity Analyst cron
slug: opportunity-analyst-cron
type: file
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: cost-budget-telemetry
    relation: uses
    description: >-
      Runs after cost-audit.py so the analyst interprets measured numbers rather
      than re-deriving them.
  - to: sentry-heartbeat
    relation: uses
    description: >-
      Reports in_progress/ok/error check-ins to the same Sentry Crons the
      heartbeat uses.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry point for the Opportunity Analyst (APP-221), selecting between the legacy in-container Codex engine and the one-shot jcode pilot container. Enforces a codex-idle guard to avoid CPU/token contention, reports liveness to Sentry Crons, refreshes live scripts/tests from the prod container (the image bakes stale copies), and resolves the image tag with a fallback because 'pilot' is frequently pruned by docker-prune-safe. Includes a byte-identical rollback path and records peak cgroup memory.

## Related

- uses [[cost-budget-telemetry]] — Runs after cost-audit.py so the analyst interprets measured numbers rather than re-deriving them.
- uses [[sentry-heartbeat]] — Reports in_progress/ok/error check-ins to the same Sentry Crons the heartbeat uses.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
