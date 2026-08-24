---
name: Operator escalation
slug: operator-escalation
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
sources_digest: 77ee937b66f808cce783fb8db16b2377efe22ed291c30d9399ba8c231ef44a42
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: apply_cycle_escalation/_consume_escalation functions
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

One-shot operator escalation (APP-238): a PENDING directive arms an escalation that is consumed exactly once; a refusal leaves it ARMED rather than burning an approval. Escalation is refused for Codex-routed cycles.

## Related

- part of [[auto-loop-core-engine]] — apply_cycle_escalation/_consume_escalation functions
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
