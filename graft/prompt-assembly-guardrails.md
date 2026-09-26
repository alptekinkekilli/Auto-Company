---
name: prompt assembly guardrails
slug: prompt-assembly-guardrails
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: 9912016534c0dfcbd55cd696d2e798e3169ab49c537a6ff43b793121e3efed5f
links:
  - to: auto-loop-core-engine
    relation: validates
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Every FULL_PROMPT assignment must assemble correctly despite embedded guardrail text, with a fixed XML section order (rules → consensus → snapshot → cycle_orders) and required headers; a stray double quote previously closed the assignment early causing a production outage that bash -n could not detect.

## Related

- validates [[auto-loop-core-engine]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
