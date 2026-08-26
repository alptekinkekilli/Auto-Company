---
name: Prompt transport contract
slug: prompt-transport-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 8047ae1ceb7eac76beba89e0584912e2500baee4f68bb2f372c872739a2c7193
sources_digest: 09490ff62dd4b45d3340d0b71341695ef1b4205f1305a986d18cf8036c7ab394
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: >-
      run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle implement this
      contract.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cycle prompts are passed via STDIN (codex uses the '-' sentinel) not argv, to avoid E2BIG; jcode refuses prompts ≥126000 bytes with a named PROMPT-TOO-LARGE reason. Prompt assembly must keep XML section order and survive embedded guardrail quotes.

## Related

- part of [[auto-loop-core-engine]] — run_claude_cycle_cli/run_codex_cycle_cli/run_jcode_cycle implement this contract.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
