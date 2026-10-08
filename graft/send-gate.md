---
name: send gate
slug: send-gate
type: system
sources:
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: b9c595d31d560e66deb88d9d01033008661c0417a03fba124ffaf1729c7c63a4
links:
  - to: g4-check
    relation: uses
    description: g4_live is stubbed in tests but called in production
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

send-gate.py is the fail-closed outreach refusal gate: daily/total caps (3/20), duplicate outreach, opt-out detection, non-Qualified status, missing email, G4 failure, TEST rows excluded by STATUS, unrendered rows, GROUP_ROUTED special case requiring full registered title and karar no, self-contradictory rows, exclusion-ground length/English-marker checks, procurement-phase mismatch, a body-leak scanner flagging internal markers (persona names, verdict vocabulary, method/provenance), unsplit rows, follow-up mode (one authorized second contact), exact normalized firm-name matching for g4_live (rejecting token collisions), fallback to the Outreach row's Website field only when the bridge row names no domain, and phase-check scoping to first-contact sends only. It refuses on any unknown or error.

## Related

- uses [[g4-check]] — g4_live is stubbed in tests but called in production
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
