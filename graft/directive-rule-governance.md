---
name: directive & rule governance
slug: directive-rule-governance
type: system
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
sources_digest: 72dca44a648f671b33d192ba19637eb703aa6164d5968c3652a46dd92a214e9f
links:
  - to: operator-escalation-gate
    relation: uses
    description: >-
      Both read the human-directive.md and audit logs that the escalation gate's
      resolution verifiers reference.
  - to: telegram-notification-channel
    relation: uses
    description: staleness-watch sends Telegram alerts via telegram-notify.sh.
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

Watchers and auditors over the human directive and standing documentation. directive-staleness-watch.py alerts when the directive stays PENDING past a threshold (only market evidence or an explicit terminal decision can satisfy it), throttled by a persisted timestamp. directive-rule-sweep.py audits which rule-like statements exist only in ephemeral directive files and are not backed by standing docs, using a canary fixture (zibberflux) to verify the heuristic and exiting 3 on UNKNOWN rather than reporting false completeness.

## Related

- uses [[operator-escalation-gate]] — Both read the human-directive.md and audit logs that the escalation gate's resolution verifiers reference.
- uses [[telegram-notification-channel]] — staleness-watch sends Telegram alerts via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
