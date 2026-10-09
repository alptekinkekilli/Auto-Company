---
name: send gate & outreach policy
slug: send-gate-outreach-policy
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
    description: send-gate calls g4_live for firm-name matching; rfq-send must NOT use G4
  - to: prod-mechanism-guard
    relation: validates
    description: rfq-send.py must be registered in the guard and pass --check-sync
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/ops/send-gate.py is a fail-closed outreach refusal gate tested as pure policy with stubbed air()/g4_live() calls. It enforces daily/total caps, duplicate/opt-out detection, Qualified-status requirement, GROUP_ROUTED special case, self-contradiction detection, a body-leak scanner for internal markers, follow-up mode, exact normalized firm-name matching for g4_live, and phase-check scoping to first-contact sends. Related rfq-send.py is a buyer-side RFQ sender with §15 sponsor approval, ANON_DENY denylist, and no G4 gate usage.

## Related

- uses [[g4-check]] — send-gate calls g4_live for firm-name matching; rfq-send must NOT use G4
- validates [[prod-mechanism-guard]] — rfq-send.py must be registered in the guard and pass --check-sync
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
