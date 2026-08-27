---
name: Prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 022c606470caf59b9766e07697dde5326e996c4c0f5c36881fc53a41c04a8d0a
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
