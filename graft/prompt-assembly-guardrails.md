---
name: Prompt assembly guardrails
slug: prompt-assembly-guardrails
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: c0e57126c65ab4d27029068d97b9639c23c17bb164ab837f71c1146b10d4580a
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: FULL_PROMPT assembly branches
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Every FULL_PROMPT assignment must assemble despite embedded guardrail text; a stray double quote previously closed the assignment early causing a production outage that bash -n could not detect. Tests verify XML section order (rules → consensus → snapshot → cycle_orders) and required guardrail headers.

## Related

- part of [[auto-loop-core-engine]] — FULL_PROMPT assembly branches
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
