---
name: Directive staleness & rule sweep
slug: directive-staleness-rule-sweep
type: system
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
sources_digest: 72dca44a648f671b33d192ba19637eb703aa6164d5968c3652a46dd92a214e9f
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
  - symbol: read_directive
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L40-L56'
  - symbol: last_line_matching
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L59-L66'
  - symbol: main
    kind: function
    at: 'scripts/ops/directive-staleness-watch.py:L69-L165'
---
<!-- context:generated:start -->
## Summary

Two operational watchers guarding the human directive: directive-staleness-watch.py alerts when the directive stays PENDING beyond a threshold (only market evidence or an explicit terminal decision can satisfy it — the company can't produce either alone), throttling via a persisted last_notified timestamp; directive-rule-sweep.py audits which rule-like statements exist only in ephemeral directive files and aren't backed by standing docs, using a canary fixture (zibberflux) that must be flagged or the run exits 3 as UNKNOWN, and exits 3 if the live directive can't be read to avoid false completeness.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
