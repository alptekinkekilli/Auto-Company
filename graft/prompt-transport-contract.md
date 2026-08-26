---
name: Prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 0a84fe33986969ce59e5241b79bdb451749288ec9bfd6d6e516ae361148c0444
links:
  - to: auto-loop-core-engine
    relation: implements
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle honor this
      contract
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The invariant that cycle prompts are passed to engine CLIs via STDIN (codex uses the - sentinel) rather than argv, preventing E2BIG failures from Linux's 131072-byte per-argument cap. run_jcode_cycle refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason before spawning.

## Related

- implements [[auto-loop-core-engine]] — run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle honor this contract
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
