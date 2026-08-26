---
name: Fail-closed send policy
slug: fail-closed-send-policy
type: concept
sources:
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: 260cbac1d830524fefee8831ec62d8032fb6948e871229aae8fb6af3055fb10f
links:
  - to: outreach-ops-scripts
    relation: part_of
    description: send-gate.py is one of the ops scripts.
  - to: outreach-ops-test-suites
    relation: validates
    description: test_send_gate.sh stubs air()/g4_live() to test this policy as pure logic.
generator:
  version: 1
covers:
  - symbol: phase_of
    kind: function
    at: 'scripts/ops/send-gate.py:L66-L91'
  - symbol: body_claims
    kind: function
    at: 'scripts/ops/send-gate.py:L94-L101'
  - symbol: load_key
    kind: function
    at: 'scripts/ops/send-gate.py:L104-L122'
  - symbol: air
    kind: function
    at: 'scripts/ops/send-gate.py:L125-L135'
  - symbol: sent_rows
    kind: function
    at: 'scripts/ops/send-gate.py:L138-L148'
  - symbol: logged_sends
    kind: function
    at: 'scripts/ops/send-gate.py:L154-L177'
  - symbol: counts
    kind: function
    at: 'scripts/ops/send-gate.py:L180-L198'
  - symbol: opted_out
    kind: function
    at: 'scripts/ops/send-gate.py:L201-L215'
  - symbol: body_leak_scan
    kind: function
    at: 'scripts/ops/send-gate.py:L236-L244'
  - symbol: g4_live
    kind: function
    at: 'scripts/ops/send-gate.py:L247-L309'
  - symbol: decide
    kind: function
    at: 'scripts/ops/send-gate.py:L312-L544'
  - symbol: main
    kind: function
    at: 'scripts/ops/send-gate.py:L547-L583'
---
<!-- context:generated:start -->
## Summary

send-gate.py's refusal logic: refuse on any unknown or error, exclude TEST rows by STATUS rather than name, require exact normalized firm-name matching for g4_live to prevent cross-firm token collisions, and scope phase checks to first-contact sends only. Guards include daily/total caps, duplicate outreach, opt-out, non-Qualified status, missing email, G4 failure, unrendered rows, GROUP_ROUTED special case, body-leak scanner for internal markers, and fallback to the Outreach row's Website field only when the bridge row names no domain.

## Related

- part of [[outreach-ops-scripts]] — send-gate.py is one of the ops scripts.
- validates [[outreach-ops-test-suites]] — test_send_gate.sh stubs air()/g4_live() to test this policy as pure logic.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
