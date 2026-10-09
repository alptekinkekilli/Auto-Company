---
name: Opportunity Analyst cron
slug: opportunity-analyst-cron
type: file
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry point for the Opportunity Analyst (APP-221), selecting engine via ANALYST_ENGINE (default jcode) and reporting liveness to Sentry Crons. Enforces a codex-idle guard (waits up to 25 min for no codex exec processes) to avoid CPU/token contention, treating a skip as liveness failure. For the jcode path it launches a disposable container with production volumes, refreshes live scripts/tests from the prod container (the image bakes stale copies), and resolves the image tag with fallback because docker-prune-safe frequently prunes 'pilot'; a missing image is fatal (exit 5). Includes a rollback path running the old in-container script byte-identically.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
