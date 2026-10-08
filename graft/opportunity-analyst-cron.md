---
name: Opportunity analyst cron
slug: opportunity-analyst-cron
type: file
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: docker-disk-guard
    relation: depends_on
    description: >-
      The pilot image it needs is frequently pruned by docker-prune-safe, hence
      the fallback image resolution.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry point for the Opportunity Analyst (APP-221), selecting between the legacy in-container Codex engine and the newer one-shot jcode pilot container via ANALYST_ENGINE. Enforces a codex-idle guard (waits up to 25 min for no codex exec processes), refreshes live scripts/tests from the prod container since the image bakes stale copies, resolves the image tag with fallback because 'pilot' is frequently pruned by docker-prune-safe, and reports liveness to Sentry Crons. Missing image is fatal (exit 5).

## Related

- depends on [[docker-disk-guard]] — The pilot image it needs is frequently pruned by docker-prune-safe, hence the fallback image resolution.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
