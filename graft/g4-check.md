---
name: G4 check
slug: g4-check
type: file
sources:
  - path: tests/test_g4_check.sh
    hash: 426129aa4d430db932523139037190cd1c5106394e917a10fc73e29b823bc4d2
sources_digest: 3479b42197aed3dc935842f570f92dbe979db1741a919d19c8c4fce117d8490d
links:
  - to: send-gate-outreach-policy
    relation: implements
    description: g4_live is the live judge used by send-gate
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/ops/g4-check.py is pure decision logic for address/registry-id/domain anchoring, with Turkish dotted/dotless İ-ı folding that must not break matches, a coincidence guard rejecting a different address on the same street pattern, and context-dependent number matching (10-digit vergi no accepted bare, 6-digit sicil requires the word 'sicil' nearby). Test cases are drawn from real production failures (RAYELSİS, ARKENOM, MAGİM).

## Related

- implements [[send-gate-outreach-policy]] — g4_live is the live judge used by send-gate
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
