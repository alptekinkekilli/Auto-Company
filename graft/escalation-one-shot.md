---
name: escalation one-shot
slug: escalation-one-shot
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
sources_digest: 3b66f1644554ee02490bcca3eb33ba9986c91efa56e722e5aabc5f1168082f10
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: apply_cycle_escalation and helpers live in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Operator escalation (APP-238) is consumed exactly once: a PENDING directive with a Claude cycle applies model/effort/timeout overrides and consumes the ESCALATE_NEXT_CYCLE flag; a DONE directive or a Codex-routed cycle refuses and leaves it ARMED rather than burning an approval. Unrelated runtime.env keys must be preserved on consumption.

## Related

- part of [[auto-loop-core-engine]] — apply_cycle_escalation and helpers live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
