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
    relation: implements
    description: >-
      The engine cycle functions in auto-loop.sh must follow this transport
      contract
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are transported to engine CLIs via STDIN (codex uses the '-' sentinel) rather than argv, to avoid Linux's 131072-byte per-argument E2BIG cap. run_jcode_cycle refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason before spawning, while normal-size prompts go as the run subcommand's argv. This is a hard contract pinned by tests.

## Related

- implements [[auto-loop-core-engine]] — The engine cycle functions in auto-loop.sh must follow this transport contract
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
