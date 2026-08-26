---
name: Opportunity Analyst Orchestration
slug: opportunity-analyst-orchestration
type: file
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: loop-lifecycle-monitoring
    relation: uses
    description: Shares the Sentry DSN parsing pattern with sentry-heartbeat.sh.
  - to: telegram-notification-channel
    relation: uses
    description: Reports liveness to Sentry Crons via a constructed check-in URL.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry for the Opportunity Analyst (APP-221), selecting jcode or legacy codex engine, enforcing a codex-idle guard to avoid CPU/token contention, launching a disposable jcode container with production volumes, and reporting liveness to Sentry Crons. A missing image is fatal (exit 5) because docker-prune-safe frequently prunes the pilot tag.

## Related

- uses [[loop-lifecycle-monitoring]] — Shares the Sentry DSN parsing pattern with sentry-heartbeat.sh.
- uses [[telegram-notification-channel]] — Reports liveness to Sentry Crons via a constructed check-in URL.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
