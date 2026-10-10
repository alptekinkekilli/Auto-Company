---
name: G4 gate
slug: g4-gate
type: concept
sources:
  - path: tests/test_g4_check.sh
    hash: 426129aa4d430db932523139037190cd1c5106394e917a10fc73e29b823bc4d2
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: 71cfcb02b92800788196cdc449440aaa1047e42a13d6c79fbdc4e3c6efac1aa1
links:
  - to: send-gate
    relation: uses
    description: send-gate.py calls g4_live() for exact normalized firm-name matching
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

g4-check.py is pure decision logic for address/registry/domain anchoring: register address vs website address matching, MERSİS/vergi no/ticaret sicil number matching, and domain extraction that skips authority sources. Turkish dotted/dotless İ-ı folding must not break matches; a different address on the same street pattern is rejected (coincidence guard); shorter numbers need more context (10-digit vergi no accepted bare, 6-digit sicil requires the word 'sicil' nearby).

## Related

- uses [[send-gate]] — send-gate.py calls g4_live() for exact normalized firm-name matching
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
