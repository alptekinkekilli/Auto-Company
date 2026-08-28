---
name: directive-rule-sweep
slug: directive-rule-sweep
type: file
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
sources_digest: 7bacb70e08cc49d472bfba609e63a7f4e8df9fb7a2bc7910d7ef5dc94f26c63b
links: []
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

Audits which rule-like statements exist only in ephemeral directive files not backed by standing docs (PROMPT.md, CLAUDE.md, PROJECT_EVALUATION_FRAMEWORK.md). SSHes into powerupp-ts host to read live directive from Docker container. Canary fixture (zibberflux marker) verifies heuristic; if not flagged exits 3 UNKNOWN. High overlap 'probably fine' never proof, low score human-review trigger.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
