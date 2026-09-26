---
name: escalation one-shot semantics
slug: escalation-one-shot-semantics
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
sources_digest: 07f4d047fe2fa274c47d77f4866134576c8ecbc7c46d9f2e8f0e8c57b068bcbd
links:
  - to: auto-loop-core-engine
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Operator escalation (APP-238) is consumed exactly once per cycle: a PENDING directive with a Claude cycle applies model/effort/timeout overrides and consumes the ESCALATE_NEXT_CYCLE flag, while a refusal leaves it ARMED rather than burning an approval. Unrelated runtime.env keys must be preserved after consumption.

## Related

- part of [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
