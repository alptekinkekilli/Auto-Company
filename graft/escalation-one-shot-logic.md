---
name: escalation one-shot logic
slug: escalation-one-shot-logic
type: concept
sources:
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
sources_digest: 6a902fd619f9d64596e8b04b7acbcda328cabd71b0a221d5b58a19c669c27e6f
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: >-
      apply_cycle_escalation/_consume_escalation/_directive_is_pending live in
      auto-loop.sh
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Operator escalation (APP-238) is consumed exactly once: a PENDING directive with a Claude cycle applies model/effort/long-wall-timeout overrides and consumes the escalation; a DONE directive or Codex-routed cycle refuses and leaves it ARMED rather than burning an approval. Unrelated keys in runtime.env must be preserved after consumption, and a double-fire attempt is a no-op.

## Related

- part of [[auto-loop-core-engine]] — apply_cycle_escalation/_consume_escalation/_directive_is_pending live in auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
