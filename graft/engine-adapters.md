---
name: Engine Adapters
slug: engine-adapters
type: system
sources:
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
  - path: tests/test_cycle_metadata.sh
    hash: 66a21f12ac379be58cda6db2e98c410b11104c0fc2c2d8c6efdffd422dcd3988
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 7e3a0eb7f26b819e2b1dd55ce42ee645b207e17bd2c8f021a107169de6632f65
links:
  - to: auto-loop-core
    relation: part_of
    description: >-
      run_claude_cycle_cli, run_codex_cycle_cli, run_jcode_cycle,
      extract_cycle_metadata are functions in auto-loop.sh.
  - to: cost-model-hint
    relation: uses
    description: >-
      engine-usage-cost.py prices token streams; model-hint must never override
      an actual completed model.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The engine CLI adapters (claude, codex, jcode) that transport prompts and attribute cycle metadata/cost. Prompts go via STDIN (codex uses '-' sentinel) to avoid E2BIG; jcode refuses prompts >=126000 bytes with PROMPT-TOO-LARGE. Mixed-harness config attributes each cycle's metadata/cost per engine.

## Related

- part of [[auto-loop-core]] — run_claude_cycle_cli, run_codex_cycle_cli, run_jcode_cycle, extract_cycle_metadata are functions in auto-loop.sh.
- uses [[cost-model-hint]] — engine-usage-cost.py prices token streams; model-hint must never override an actual completed model.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
