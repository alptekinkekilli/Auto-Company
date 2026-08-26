---
name: analyst-engine
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
      The analyst is a separate engine path that shares the runtime.env and
      session-log conventions with the main loop.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/analyst/opportunity-analyst-jcode.sh and its offline test harness: a jcode-driven analyst that fails closed on missing credentials, reads tokens literally from runtime.env, rides provider-specific effort env vars, and dedups session ids into a sessions log.

## Related

- part of [[auto-loop-core]] — The analyst is a separate engine path that shares the runtime.env and session-log conventions with the main loop.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
