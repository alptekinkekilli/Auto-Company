---
name: prompt assembly
slug: prompt-assembly
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
sources_digest: 33b9337ae75d8fe878f55da1d39c2eadda766988f0bb1fcdd332fdd1a2362aed
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The prompt-building branches live in auto-loop.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Every FULL_PROMPT assignment must assemble correctly despite embedded guardrail text: the 'Runtime Guardrails' header, five specific rules (OUTPUT HYGIENE, TURN ECONOMY, etc.), the expanded cycle counter, turn-feedback slot, pre-run snapshot, and XML section order (rules → consensus → snapshot → cycle_orders). A stray double quote previously closed the assignment early causing a production outage that bash -n could not detect; the test evaluates each branch in a sandboxed bash -c and deliberately avoids mapfile for macOS bash 3.2 compatibility.

## Related

- part of [[auto-loop-core-engine]] — The prompt-building branches live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
