---
name: prompt assembly & transport
slug: prompt-assembly-transport
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: fc5c802aa5b5e99dff8841ee1a4b9df2c39abe8281d806c55564f4dd36753d48
links:
  - to: auto-loop-core-loop
    relation: part_of
    description: Prompt building and engine invocation are functions inside auto-loop.sh.
  - to: budget-spend-accounting
    relation: uses
    description: >-
      The discretionary daily cap injects a warning line into the prompt once
      the day's spend reaches the threshold.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Assembles the FULL_PROMPT (rules → consensus → snapshot → cycle_orders XML order) and transports it to engine CLIs: via STDIN for claude/codex (codex uses the `-` sentinel) to avoid E2BIG, and as the `run` subcommand argv for jcode with a 126000-byte refusal threshold. A stray quote/backtick/$( in guardrail text previously caused a production outage that bash -n could not catch.

## Related

- part of [[auto-loop-core-loop]] — Prompt building and engine invocation are functions inside auto-loop.sh.
- uses [[budget-spend-accounting]] — The discretionary daily cap injects a warning line into the prompt once the day's spend reaches the threshold.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
