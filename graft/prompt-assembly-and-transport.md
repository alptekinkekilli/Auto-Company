---
name: Prompt assembly and transport
slug: prompt-assembly-and-transport
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
  - to: auto-loop-core-engine
    relation: part_of
    description: Prompt-building branches live in auto-loop.sh.
  - to: set-e-lint
    relation: validates
    description: >-
      test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action
      pattern.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Assembly of FULL_PROMPT from guardrails, consensus, snapshot, and cycle_orders, and transport of that prompt to engine CLIs. Prompts go via STDIN (codex uses the - sentinel) to avoid E2BIG; run_jcode_cycle refuses prompts ≥126000 bytes with a named PROMPT-TOO-LARGE reason. A stray quote in guardrail text previously caused a production outage that bash -n could not catch.

## Related

- part of [[auto-loop-core-engine]] — Prompt-building branches live in auto-loop.sh.
- validates [[set-e-lint]] — test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action pattern.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
