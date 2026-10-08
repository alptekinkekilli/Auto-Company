---
name: Directive rule sweep
slug: directive-rule-sweep
type: file
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
sources_digest: 7bacb70e08cc49d472bfba609e63a7f4e8df9fb7a2bc7910d7ef5dc94f26c63b
links:
  - to: human-directive-writer
    relation: validates
    description: >-
      Audits the live container directive against standing docs, mirroring the
      trust-gating pattern of the leak scanner's selftest.
generator:
  version: 1
covers:
  - symbol: key_phrases
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L49-L52'
  - symbol: covered
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L55-L68'
---
<!-- context:generated:start -->
## Summary

Audits which rule-like statements exist only in ephemeral directive files and are not backed by standing documentation, using token-overlap heuristics that treat high scores as 'probably fine' but never proof. Relies on a canary fixture (zibberflux marker) to verify the heuristic still works — if the canary is not flagged, or the live directive cannot be read, the run exits 3 and reports coverage as UNKNOWN to avoid false completeness.

## Related

- validates [[human-directive-writer]] — Audits the live container directive against standing docs, mirroring the trust-gating pattern of the leak scanner's selftest.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
