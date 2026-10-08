---
name: prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 43a23a58000634ae27009c31c7b63ef340a08366539358de968d0fd597edf089
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle live in
      auto-loop.sh
  - to: prompt-assembly-contract
    relation: uses
    description: Transports the assembled FULL_PROMPT
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are passed to engine CLIs via STDIN (codex uses the '-' sentinel) rather than as argv, preventing E2BIG failures from Linux's 131072-byte per-argument cap. run_jcode_cycle refuses prompts ≥126000 bytes with a named PROMPT-TOO-LARGE reason before spawning, while passing normal-size prompts as the run subcommand's argv.

## Related

- part of [[auto-loop-core-engine]] — run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle live in auto-loop.sh
- uses [[prompt-assembly-contract]] — Transports the assembled FULL_PROMPT
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
