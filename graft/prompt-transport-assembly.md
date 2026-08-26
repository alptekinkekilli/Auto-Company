---
name: Prompt transport & assembly
slug: prompt-transport-assembly
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: edfd9b24c35ca741a1773b2f381e9bb74edd5e3db974985005d0a7805c91226b
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Prompt assembly and transport functions live in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Builds the FULL_PROMPT for each cycle (rules → consensus → snapshot → cycle_orders XML order) and transports it to engine CLIs via STDIN (codex uses the `-` sentinel) rather than argv, avoiding E2BIG. run_jcode_cycle refuses prompts ≥126000 bytes with a named PROMPT-TOO-LARGE reason before spawning.

## Related

- part of [[auto-loop-core-engine]] — Prompt assembly and transport functions live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
