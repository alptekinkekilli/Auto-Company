---
name: cycle metadata extraction
slug: cycle-metadata-extraction
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: tests/test_cycle_metadata.sh
    hash: 66a21f12ac379be58cda6db2e98c410b11104c0fc2c2d8c6efdffd422dcd3988
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: b71af85a8e3d37ddedc24ebaad80325f373a40d492b8573185b04ec3236f0e13
links:
  - to: auto-loop-core-loop
    relation: part_of
    description: extract_cycle_metadata() and run_engine_cycle() live in auto-loop.sh.
  - to: budget-spend-accounting
    relation: uses
    description: Per-cycle cost attribution feeds record_total_spend and the ledger.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Parses engine output into CYCLE_TYPE/CYCLE_SUBTYPE/RESULT_TEXT and attributes each cycle's harness/provider/cost. Must be robust under set -euo pipefail (APP-240 regression: plain-prose Codex output used to kill the loop) and must attribute mixed-harness cycles correctly, persisting a claude attempt's cost under its own run ID before a codex retry (REVISE-2 gate A5).

## Related

- part of [[auto-loop-core-loop]] — extract_cycle_metadata() and run_engine_cycle() live in auto-loop.sh.
- uses [[budget-spend-accounting]] — Per-cycle cost attribution feeds record_total_spend and the ledger.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
