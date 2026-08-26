---
name: prompt transport & assembly safety
slug: prompt-transport-assembly-safety
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 4b9d5d46f953db128f3b0708441a0d3b6c32e662d7c6187047f6f2dfaa2ab429
links:
  - to: auto-loop-core
    relation: implements
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle implement this
      contract.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are assembled with embedded guardrail text and transported to engine CLIs via STDIN (codex uses the '-' sentinel) rather than argv to avoid E2BIG; jcode refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason. A stray quote/backtick/$() in guardrails must fail the prompt-assembly test, not production.

## Related

- implements [[auto-loop-core]] — run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle implement this contract.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
