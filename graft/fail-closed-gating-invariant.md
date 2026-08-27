---
name: Fail-closed gating invariant
slug: fail-closed-gating-invariant
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: scripts/ops/rfq-send.py
    hash: 9f7b4a48afe6563f777bfe314209d32a3bc0343d178e25ecf0a442cac0ced2e5
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
sources_digest: c280756b3372ffed42aee3ec59d8545809e3d528a27de1f97adf09952a6894bf
links:
  - to: auto-loop-core
    relation: implements
    description: ccusage and budget gates latch holds on degraded reads.
  - to: send-gate
    relation: implements
    description: Send gate's decide() returns REFUSE on any incomplete check.
generator:
  version: 1
covers:
  - symbol: _load_key
    kind: function
    at: 'scripts/ops/rfq-send.py:L90-L111'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/rfq-send.py:L114-L116'
  - symbol: _air
    kind: function
    at: 'scripts/ops/rfq-send.py:L120-L132'
  - symbol: _record
    kind: function
    at: 'scripts/ops/rfq-send.py:L135-L136'
  - symbol: _all_rows
    kind: function
    at: 'scripts/ops/rfq-send.py:L139-L150'
  - symbol: _sponsor_ok
    kind: function
    at: 'scripts/ops/rfq-send.py:L154-L155'
  - symbol: _opted_out
    kind: function
    at: 'scripts/ops/rfq-send.py:L158-L159'
  - symbol: _already_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L162-L163'
  - symbol: _email_of
    kind: function
    at: 'scripts/ops/rfq-send.py:L166-L168'
  - symbol: _caps_now
    kind: function
    at: 'scripts/ops/rfq-send.py:L171-L181'
  - symbol: render
    kind: function
    at: 'scripts/ops/rfq-send.py:L184-L191'
  - symbol: anonymity_scan
    kind: function
    at: 'scripts/ops/rfq-send.py:L194-L199'
  - symbol: decide
    kind: function
    at: 'scripts/ops/rfq-send.py:L202-L224'
  - symbol: _encode_subject
    kind: function
    at: 'scripts/ops/rfq-send.py:L228-L231'
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L234-L249'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L252-L255'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L259-L301'
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

Across the RFQ send, send-gate, budget gates, ccusage measurement, and MCP probe, the system's core invariant is fail-closed: any check that cannot complete, any degraded read, any missing credential, or any malformed input must produce a REFUSE/NA/hold, never an ALLOW or a zero. This is incident-driven hardening.

## Related

- implements [[auto-loop-core]] — ccusage and budget gates latch holds on degraded reads.
- implements [[send-gate]] — Send gate's decide() returns REFUSE on any incomplete check.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
