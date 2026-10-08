---
name: Opportunity Analyst cron
slug: opportunity-analyst-cron
type: file
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: budget-calibration-cost-audit
    relation: uses
    description: Runs after cost-audit.py writes memories/cost-audit.md.
  - to: docker-disk-space-guard-docker-prune-safe
    relation: depends_on
    description: >-
      Must handle the pilot image being pruned by docker-prune-safe via fallback
      image resolution.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry point for the Opportunity Analyst (APP-221), selecting engine via ANALYST_ENGINE (default jcode), reporting liveness to Sentry Crons, and enforcing a codex-idle guard (waits up to 25 min for no codex exec processes) to avoid CPU/token contention. For the jcode path it launches a disposable container with production volumes mounted, mirrors the /app/docs symlink, refreshes live scripts/tests from the prod container (image bakes stale copies), and resolves the image tag with fallback to any available autocompany-jcode image because pilot is frequently pruned by docker-prune-safe; a missing image is fatal (exit 5). Includes a rollback path (ANALYST_ENGINE=codex) running the old in-container script byte-identically.

## Related

- uses [[budget-calibration-cost-audit]] — Runs after cost-audit.py writes memories/cost-audit.md.
- depends on [[docker-disk-space-guard-docker-prune-safe]] — Must handle the pilot image being pruned by docker-prune-safe via fallback image resolution.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
