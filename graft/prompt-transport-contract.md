---
name: prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 7641edc5e6cf3595d6ba2c87272acee0e6d7898c1b2985ba99881678a01a0ffc
links:
  - to: auto-loop-sh-core-loop
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are transported to engine CLIs via STDIN (codex uses '-' sentinel) to avoid E2BIG from the 131072-byte argv cap; jcode refuses prompts ≥126000 bytes with PROMPT-TOO-LARGE before spawning.

## Related

- part of [[auto-loop-sh-core-loop]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
