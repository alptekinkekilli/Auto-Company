---
name: Directive governance watchers
slug: directive-governance-watchers
type: system
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
sources_digest: 72dca44a648f671b33d192ba19637eb703aa6164d5968c3652a46dd92a214e9f
links:
  - to: trust-gating-canary-pattern
    relation: implements
    description: >-
      directive-rule-sweep's canary fixture and exit-3 gate mirror
      bridge_leak_scan's selftest gate.
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

Operational watchers around the human directive. directive-rule-sweep.py audits which rule-like statements exist only in ephemeral directive files and are not backed by standing documentation, using a token-overlap heuristic that treats high score as 'probably fine' but never proof, with a canary fixture (zibberflux marker) that exits 3 if not flagged and exits 3 if the live directive can't be read (avoiding false completeness). directive-staleness-watch.py alerts when the directive stays PENDING beyond a threshold (default 12h), because the completion clause can only be satisfied by market evidence or an explicit terminal decision — neither of which the company can produce alone; it never edits or clears the directive, only reports, and re-notifies at most every --repeat-hours.

## Related

- implements [[trust-gating-canary-pattern]] — directive-rule-sweep's canary fixture and exit-3 gate mirror bridge_leak_scan's selftest gate.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
