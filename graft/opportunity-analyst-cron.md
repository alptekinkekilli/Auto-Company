---
name: opportunity-analyst-cron
slug: opportunity-analyst-cron
type: file
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
sources_digest: 927a3e73b4ddafbf79191ec84e859e236b432d3379234edb4566977f1c47dddb
links:
  - to: docker-prune-safe
    relation: depends_on
    description: >-
      Image tag fallback exists because docker-prune-safe frequently prunes the
      pilot image.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Daily cron entry for Opportunity Analyst (APP-221), selecting legacy in-container Codex or one-shot jcode pilot via ANALYST_ENGINE. Reports liveness to Sentry Crons. Enforces codex-idle guard (25min wait) to avoid CPU/token contention. jcode path launches disposable container, refreshes live scripts/tests from prod (image bakes stale copies), resolves image tag with fallback (pilot frequently pruned by docker-prune-safe); missing image fatal exit 5. Rollback path runs old script byte-identically.

## Related

- depends on [[docker-prune-safe]] — Image tag fallback exists because docker-prune-safe frequently prunes the pilot image.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
