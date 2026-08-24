---
name: Prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: b0a1706e8620bb1087ab074cacb8ebf1a3dec5910df6dff7b0e9274d66d4b276
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: functions run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are transported to engine CLIs via STDIN (codex uses the `-` sentinel) rather than argv, to avoid Linux's 131072-byte per-argument E2BIG cap. run_jcode_cycle refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason before spawning.

## Related

- part of [[auto-loop-core-engine]] — functions run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
