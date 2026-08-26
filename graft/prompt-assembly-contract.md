---
name: Prompt assembly contract
slug: prompt-assembly-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: d52802f9bd10db20b4abd223179e1db74a972827d591949478f7fa57c2e7bc7e
links:
  - to: auto-loop-sh-core-loop
    relation: validates
    description: >-
      test_prompt_assembly.sh extracts each prompt-building branch and evaluates
      it in a sandboxed bash -c.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Every FULL_PROMPT assignment must assemble correctly despite embedded guardrail text, containing the Runtime Guardrails header, five specific rules, the expanded cycle counter, the turn-feedback slot, the pre-run snapshot, and XML sections in order rules → consensus → snapshot → cycle_orders. A stray double quote previously closed the assignment early and caused a production outage that bash -n could not detect.

## Related

- validates [[auto-loop-sh-core-loop]] — test_prompt_assembly.sh extracts each prompt-building branch and evaluates it in a sandboxed bash -c.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
