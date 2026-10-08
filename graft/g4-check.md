---
name: G4 check
slug: g4-check
type: concept
sources:
  - path: tests/test_g4_check.sh
    hash: 426129aa4d430db932523139037190cd1c5106394e917a10fc73e29b823bc4d2
sources_digest: 3479b42197aed3dc935842f570f92dbe979db1741a919d19c8c4fce117d8490d
links:
  - to: send-gate
    relation: uses
    description: send-gate.py calls g4_live for firm-name matching
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

g4-check.py matches register addresses against website addresses with Turkish dotted/dotless İ-ı folding that must not break matches, a coincidence guard rejecting a different address on the same street pattern, and context-dependent number anchoring: a 10-digit vergi no is accepted bare while a 6-digit sicil requires the word 'sicil' nearby. Domain extraction skips authority sources like kik.gov.tr and mersis.ticaret.gov.tr. Cases are drawn from real production failures (RAYELSİS, ARKENOM, MAGİM).

## Related

- uses [[send-gate]] — send-gate.py calls g4_live for firm-name matching
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
