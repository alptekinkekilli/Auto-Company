---
name: prompt assembly contract
slug: prompt-assembly-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: 00bfd4f3c4378bce74ae9c21c517d30442d7649bc2e9bf9d3086fd4fddab4924
links:
  - to: auto-loop-sh-core-loop
    relation: part_of
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Every FULL_PROMPT assignment must assemble correctly despite embedded guardrail text: Runtime Guardrails header, five rules, expanded cycle counter, turn-feedback slot, pre-run snapshot, and XML section order (rules → consensus → snapshot → cycle_orders). A stray quote/backtick/$() must fail here, not in production.

## Related

- part of [[auto-loop-sh-core-loop]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
