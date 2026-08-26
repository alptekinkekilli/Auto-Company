---
name: Prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 784a97c5426b950cf3ba16542c92830014f14cdb63b07e34995ef319dd7d6e26
links:
  - to: auto-loop-sh-core-loop
    relation: validates
    description: >-
      test_prompt_transport.sh extracts the transport function bodies and runs
      them against a stub engine binary.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are transported to engine CLIs via STDIN (codex uses the `-` sentinel) rather than as an argv argument, avoiding Linux's 131072-byte per-argument E2BIG cap. run_jcode_cycle refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason before spawning, while passing normal-size prompts as the run subcommand's argv.

## Related

- validates [[auto-loop-sh-core-loop]] — test_prompt_transport.sh extracts the transport function bodies and runs them against a stub engine binary.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
