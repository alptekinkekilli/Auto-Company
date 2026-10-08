---
name: Directive rule sweep
slug: directive-rule-sweep
type: system
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
sources_digest: 7bacb70e08cc49d472bfba609e63a7f4e8df9fb7a2bc7910d7ef5dc94f26c63b
links:
  - to: directive-writer-human-directive-md
    relation: validates
    description: Audits the live container directive body against standing docs.
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

Audits which rule-like statements exist only in ephemeral directive files and are not backed by standing documentation. Uses a token-overlap heuristic that treats high coverage as 'probably fine' but never proof, and relies on a canary fixture (zibberflux marker) — if the canary is not flagged, or the live directive cannot be read, it exits 3 and reports UNKNOWN to avoid false completeness.

## Related

- validates [[directive-writer-human-directive-md]] — Audits the live container directive body against standing docs.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
