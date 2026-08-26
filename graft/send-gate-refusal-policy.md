---
name: send-gate refusal policy
slug: send-gate-refusal-policy
type: file
sources:
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: bece9baf8d16a069f62e22ae4b1642a00f1e292f3d95998c50484f4786603492
links:
  - to: offline-stubbing-test-pattern
    relation: validates
    description: Its 20 refusal scenarios are pinned by stubbing air() and g4_live().
  - to: ops-watchers-audit-scripts
    relation: part_of
    description: >-
      send-gate is one of the ops scripts, tested offline via the stubbing
      pattern.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

send-gate.py is the fail-closed outreach gate: it refuses on any unknown/error and enforces ~20 guards including daily/total caps, duplicate outreach, opt-out, non-Qualified status, missing email, G4 failure, TEST-row exclusion by STATUS (not name), unrendered rows, the GROUP_ROUTED special case requiring full registered title + karar no, self-contradictory rows, a body-leak scanner for internal markers, unsplit rows, follow-up mode (one authorized second contact), exact normalized firm-name matching for g4_live (rejecting token collisions), and Website-field fallback only when the bridge row names no domain. Phase-check scoping applies to first-contact sends only.

## Related

- validates [[offline-stubbing-test-pattern]] — Its 20 refusal scenarios are pinned by stubbing air() and g4_live().
- part of [[ops-watchers-audit-scripts]] — send-gate is one of the ops scripts, tested offline via the stubbing pattern.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
