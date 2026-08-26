---
name: Prompt assembly guardrails
slug: prompt-assembly-guardrails
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: b721c057b1ae1890115e0e638f6ef3f615c7f1a33cef1e0f9ef3e1e65d29eaa6
links:
  - to: auto-loop-core-engine
    relation: implements
    description: The prompt-building branches in auto-loop.sh
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The invariant that every FULL_PROMPT assignment assembles correctly despite embedded guardrail text, with a specific XML section order (rules → consensus → snapshot → cycle_orders). Exists because a stray double quote previously closed the assignment early causing a production outage that bash -n could not detect.

## Related

- implements [[auto-loop-core-engine]] — The prompt-building branches in auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
