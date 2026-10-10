---
name: prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: f9fdd724bb168be925b2b29efa01334460fdf2724e6d4d8edae39a2e53679aba
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The transport functions and FULL_PROMPT assembly live in auto-loop.sh
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are transported to engine CLIs via STDIN (codex uses the '-' sentinel) rather than argv, preventing E2BIG failures from Linux's 131072-byte per-argument cap. run_jcode_cycle refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason before spawning. Prompt assembly must preserve XML section order (rules → consensus → snapshot → cycle_orders) and survive embedded guardrail text.

## Related

- part of [[auto-loop-core-engine]] — The transport functions and FULL_PROMPT assembly live in auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
