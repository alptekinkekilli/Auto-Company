---
name: Operator Escalation
slug: operator-escalation
type: system
sources:
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
sources_digest: 6a902fd619f9d64596e8b04b7acbcda328cabd71b0a221d5b58a19c669c27e6f
links:
  - to: auto-loop-core
    relation: part_of
    description: >-
      apply_cycle_escalation, _consume_escalation, _directive_is_pending are
      functions in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

One-shot operator escalation logic (APP-238): an escalation is consumed exactly once, and a refusal leaves it ARMED rather than burning an approval. Reads runtime.env keys and human-directive.md pending state.

## Related

- part of [[auto-loop-core]] — apply_cycle_escalation, _consume_escalation, _directive_is_pending are functions in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
