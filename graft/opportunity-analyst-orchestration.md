---
name: Opportunity Analyst Orchestration
slug: opportunity-analyst-orchestration
type: system
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: compliance-audit-watchers
    relation: uses
    description: >-
      Refreshes live scripts/tests from the prod container since the image bakes
      stale copies.
  - to: telegram-notification-channel
    relation: uses
    description: Reports liveness to Sentry Crons via a constructed check-in URL.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The daily cron entry point for the Opportunity Analyst (APP-221), selecting jcode or legacy codex engine, reporting liveness to Sentry Crons, enforcing a codex-idle guard, launching a disposable container with production volumes, and resolving the image tag with fallback because pilot is frequently pruned by docker-prune-safe. Includes a rollback path running the old in-container script byte-identically.

## Related

- uses [[compliance-audit-watchers]] — Refreshes live scripts/tests from the prod container since the image bakes stale copies.
- uses [[telegram-notification-channel]] — Reports liveness to Sentry Crons via a constructed check-in URL.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
