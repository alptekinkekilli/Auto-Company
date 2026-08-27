---
name: Analyst engine runner
slug: analyst-engine-runner
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
sources_digest: 7f8e7d6a9e197732a06d93ee9f99e03a2a50ef0721c7d992f3621f154f72a6b3
links:
  - to: auto-loop-core-auto-loop-sh
    relation: uses
    description: >-
      Analyst sessions excluded from budget gates; report hash delta-visible in
      snapshot.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

opportunity-analyst-jcode.sh runs the analyst cycle via jcode, failing closed on missing credentials, riding provider-specific effort env vars, deduping session IDs into analyst-jcode-sessions.log, and writing the report header to analysis-directive.md.

## Related

- uses [[auto-loop-core-auto-loop-sh]] — Analyst sessions excluded from budget gates; report hash delta-visible in snapshot.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
