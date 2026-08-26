---
name: escalation & one-shot consumption
slug: escalation-one-shot-consumption
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
sources_digest: 9390cd3a10c417b42cb8ec1b1d5f534a8130d315d55b6c4f5475bff2333859bc
links:
  - to: auto-loop-core
    relation: implements
    description: apply_cycle_escalation/_consume_escalation.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Operator escalations are consumed exactly once; a refusal leaves the escalation ARMED rather than burning an approval, and unrelated runtime.env keys are preserved after consumption.

## Related

- implements [[auto-loop-core]] — apply_cycle_escalation/_consume_escalation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
