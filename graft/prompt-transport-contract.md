---
name: prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 646a4ca1b33c9257534c458f8bcc8c5a7246acca853acc71ad0ec444d8b03f1d
links:
  - to: auto-loop-core-engine
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are passed to engine CLIs via STDIN (codex uses the `-` sentinel) rather than argv, to avoid Linux's 131072-byte per-argument E2BIG cap; run_jcode_cycle refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason before spawning. This is pinned by test_prompt_transport.sh.

## Related

- part of [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
