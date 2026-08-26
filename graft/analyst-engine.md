---
name: Analyst engine
slug: analyst-engine
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
sources_digest: 7f8e7d6a9e197732a06d93ee9f99e03a2a50ef0721c7d992f3621f154f72a6b3
links:
  - to: auto-loop-core-engine
    relation: uses
    description: >-
      Analyst sessions are excluded from budget gates and run as a separate
      engine.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

opportunity-analyst-jcode.sh runs the analyst cycle via jcode, with provider-specific env vars for effort, fail-closed credential checks, and session-id dedup into analyst-jcode-sessions.log.

## Related

- uses [[auto-loop-core-engine]] — Analyst sessions are excluded from budget gates and run as a separate engine.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
