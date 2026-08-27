---
name: Analyst engine & escalation
slug: analyst-engine-escalation
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
sources_digest: 7374c949b566eaeb00521ceadbf9646b4e21b1c06da568ce668e3236e9022224
links:
  - to: auto-loop-core-engine
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The opportunity-analyst jcode harness and one-shot operator escalation: escalation is consumed exactly once, a refusal leaves it ARMED, and provider-specific env vars (effort, model) ride without leaking. The analyst harness fails closed naming the missing credential.

## Related

- part of [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
