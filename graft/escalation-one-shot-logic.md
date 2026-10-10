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
    description: Escalation functions live in auto-loop.sh
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

One-shot operator escalation (APP-238): an escalation is consumed exactly once, and a refusal leaves it ARMED rather than burning an approval. Functions apply_cycle_escalation, _read_runtime_env_key, _consume_escalation, _directive_is_pending. A PENDING directive with a Claude cycle triggers model override, effort override, long wall timeout, and consumption; a DONE directive is refused and stays armed; unrelated keys in runtime.env are preserved after consumption.

## Related

- part of [[auto-loop-core-engine]] — Escalation functions live in auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
