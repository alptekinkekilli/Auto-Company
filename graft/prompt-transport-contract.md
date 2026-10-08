---
name: prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: e7fd03ea1456eec057808ab130ab80d2b681c1941b7111fd30f9240e200f4451
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The transport functions live in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are transported to engine CLIs via STDIN (codex uses the '-' sentinel) rather than argv, to avoid Linux's 131072-byte per-argument E2BIG cap. run_jcode_cycle refuses prompts >=126000 bytes with a named PROMPT-TOO-LARGE reason before spawning, while normal-size prompts go as the run subcommand's argv. This contract is pinned by tests that stub the engine binary and record argv/stdin.

## Related

- part of [[auto-loop-core-engine]] — The transport functions live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
