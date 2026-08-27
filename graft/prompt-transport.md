---
name: prompt_transport
slug: prompt-transport
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 022c606470caf59b9766e07697dde5326e996c4c0f5c36881fc53a41c04a8d0a
links:
  - to: auto-loop
    relation: validates
    description: >-
      test_prompt_transport extracts and runs the run_*_cycle_cli bodies against
      a stub engine to pin the STDIN contract.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The invariant that cycle prompts are delivered to engine CLIs via STDIN (codex via '-' sentinel) rather than argv, preventing E2BIG failures from Linux's 131072-byte per-argument cap; jcode additionally refuses prompts ≥126000 bytes with a named PROMPT-TOO-LARGE reason before spawning.

## Related

- validates [[auto-loop]] — test_prompt_transport extracts and runs the run_*_cycle_cli bodies against a stub engine to pin the STDIN contract.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
