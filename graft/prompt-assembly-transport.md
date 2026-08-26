---
name: Prompt assembly & transport
slug: prompt-assembly-transport
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: 4b9d5d46f953db128f3b0708441a0d3b6c32e662d7c6187047f6f2dfaa2ab429
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: Prompt assembly and transport are functions of auto-loop.sh.
  - to: state-snapshot-probe
    relation: uses
    description: The pre-run snapshot is embedded in the prompt.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The FULL_PROMPT assembly branches in auto-loop.sh and the transport contract to engine CLIs: prompts go via STDIN (codex uses the '-' sentinel) to avoid E2BIG, jcode refuses prompts >=126000 bytes with PROMPT-TOO-LARGE, and the XML section order (rules → consensus → snapshot → cycle_orders) is pinned. A stray quote in guardrail text previously caused a production outage that bash -n could not catch.

## Related

- part of [[auto-loop-core-engine]] — Prompt assembly and transport are functions of auto-loop.sh.
- uses [[state-snapshot-probe]] — The pre-run snapshot is embedded in the prompt.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
