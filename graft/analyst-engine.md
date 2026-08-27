---
name: Analyst engine
slug: analyst-engine
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
sources_digest: 24e5cf415f1f3114f9283e91276213f80f34d7f0fcc25c5d4753b7b247f1c154
links:
  - to: auto-loop-core
    relation: part_of
    description: >-
      Analyst cycles are excluded from budget gates and run through this
      harness.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The opportunity-analyst jcode harness that runs the analyst cycle, reading credentials from runtime.env or openai-auth.json, riding provider-specific effort env vars, and writing a deduped session log and report header.

## Related

- part of [[auto-loop-core]] — Analyst cycles are excluded from budget gates and run through this harness.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
