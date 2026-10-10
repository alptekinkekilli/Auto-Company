---
name: send gate
slug: send-gate
type: file
sources:
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: bece9baf8d16a069f62e22ae4b1642a00f1e292f3d95998c50484f4786603492
links:
  - to: g4-gate
    relation: uses
    description: Calls g4_live() for firm-name matching; refuses on G4 failure
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

send-gate.py is a fail-closed outreach gate refusing on any unknown or error across 20 scenarios: daily/total caps, duplicate outreach, opt-out, non-Qualified status, missing email, G4 failure, TEST rows excluded by STATUS, unrendered rows, GROUP_ROUTED requiring full registered title and karar no, self-contradictory rows, procurement-phase mismatch, a body-leak scanner for internal markers, unsplit rows, follow-up mode (one authorized second contact), exact normalized firm-name matching for g4_live, fallback to Website field only when bridge row names no domain, and phase-check scoping to first-contact sends.

## Related

- uses [[g4-gate]] — Calls g4_live() for firm-name matching; refuses on G4 failure
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
