---
name: Opportunity Analyst cron
slug: opportunity-analyst-cron
type: system
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: docker-disk-space-guard
    relation: depends_on
    description: >-
      The pilot image it needs is frequently pruned by docker-prune-safe, hence
      the fallback resolution.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry for the Opportunity Analyst (APP-221), selecting legacy in-container Codex or one-shot jcode pilot container via ANALYST_ENGINE. Enforces a codex-idle guard (waits up to 25 min for no codex exec processes) to avoid CPU/token contention, refreshes live scripts/tests from the prod container since the image bakes stale copies, and resolves the image tag with fallback because 'pilot' is frequently pruned by docker-prune-safe. Reports liveness to Sentry Crons with in_progress/ok/error.

## Related

- depends on [[docker-disk-space-guard]] — The pilot image it needs is frequently pruned by docker-prune-safe, hence the fallback resolution.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
