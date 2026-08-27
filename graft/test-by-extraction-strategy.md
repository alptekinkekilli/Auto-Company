---
name: Test-by-extraction strategy
slug: test-by-extraction-strategy
type: concept
sources:
  - path: tests/test_airtable_write.sh
    hash: a51c25001935da566cca4a450cfc0906827eb332779f2b454b12d547b7a0e6e0
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_g4_check.sh
    hash: 426129aa4d430db932523139037190cd1c5106394e917a10fc73e29b823bc4d2
sources_digest: c7ce47c0a5f7f19156e3e5619423d8e295ecd6689316713e3dbdf6bc7b6011c2
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Tests extract real function bodies from auto-loop.sh via awk/sed rather than reimplementing, so any change to extraction patterns breaks loudly. Same strategy for g4-check, directive_writer, airtable guards.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
