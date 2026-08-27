---
name: Analyst engine runner
slug: analyst-engine-runner
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
sources_digest: 24e5cf415f1f3114f9283e91276213f80f34d7f0fcc25c5d4753b7b247f1c154
links:
  - to: auto-loop-orchestration-core
    relation: uses
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

opportunity-analyst-jcode.sh runs the analyst jcode cycle with provider-specific credential/effort handling, deduping session IDs into analyst-jcode-sessions.log and writing the report header into analysis-directive.md.

## Related

- uses [[auto-loop-orchestration-core]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
