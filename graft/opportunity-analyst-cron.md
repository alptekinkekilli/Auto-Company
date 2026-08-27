---
name: Opportunity Analyst cron
slug: opportunity-analyst-cron
type: system
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: sentry-heartbeat
    relation: uses
    description: Reports liveness to Sentry Crons via a constructed check-in URL.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry point for the Opportunity Analyst (APP-221), orchestrating either the legacy in-container Codex engine or the newer one-shot jcode pilot container. Enforces a codex-idle guard (waits up to 25 min for no codex exec processes) to avoid CPU/token contention, reports liveness to Sentry Crons, and refreshes live scripts/tests from the prod container since the image bakes stale copies. Includes a rollback path (ANALYST_ENGINE=codex) running the old script byte-identically.

## Related

- uses [[sentry-heartbeat]] — Reports liveness to Sentry Crons via a constructed check-in URL.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
