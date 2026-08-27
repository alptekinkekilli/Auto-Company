---
name: Never-twice / dedup invariant
slug: never-twice-dedup-invariant
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: scripts/ops/rfq-send.py
    hash: 9f7b4a48afe6563f777bfe314209d32a3bc0343d178e25ecf0a442cac0ced2e5
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
sources_digest: 85d742a647f15de434c2d06572c4c99649e28768968599d56d1684d4b0f75fde
links:
  - to: rfq-send-pipeline
    relation: implements
    description: Never-twice gate via Durum/Gönderim TS.
  - to: send-gate
    relation: implements
    description: Never-send-twice via log-derived sends.
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

The system must never contact the same firm twice: RFQ send gates on Durum/Gönderim TS, send-gate parses Sent: entries from the Email log rather than trusting row counts, and the cycle counter is monotonic across redeploys. Dedup is keyed on content, not names, because counters restart on container restart.

## Related

- implements [[rfq-send-pipeline]] — Never-twice gate via Durum/Gönderim TS.
- implements [[send-gate]] — Never-send-twice via log-derived sends.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
