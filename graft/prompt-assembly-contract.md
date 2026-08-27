---
name: Prompt assembly contract
slug: prompt-assembly-contract
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: e8cd96191dd830ff7d1230db371cd214965460659eec8c4eec0a5365fc14376d
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
