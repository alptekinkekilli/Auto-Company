---
name: prompt assembly contract
slug: prompt-assembly-contract
type: concept
sources:
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: 337bc3bba0446f2f993e76a61a778312b8e85fb03f049e8a0986c6883b785dcc
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: FULL_PROMPT assignments live in auto-loop.sh
  - to: prompt-transport-contract
    relation: produces
    description: The assembled prompt is what gets transported to engine CLIs
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Every FULL_PROMPT assignment must assemble correctly despite embedded guardrail text — a stray double quote previously closed the assignment early causing a production outage that bash -n could not detect. Required elements: 'Runtime Guardrails' header, five specific rules (OUTPUT HYGIENE, TURN ECONOMY, etc.), expanded cycle counter, turn-feedback slot, pre-run snapshot, and correct XML section order (rules → consensus → snapshot → cycle_orders). Must avoid mapfile for macOS bash 3.2 compatibility.

## Related

- part of [[auto-loop-core-engine]] — FULL_PROMPT assignments live in auto-loop.sh
- produces [[prompt-transport-contract]] — The assembled prompt is what gets transported to engine CLIs
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
