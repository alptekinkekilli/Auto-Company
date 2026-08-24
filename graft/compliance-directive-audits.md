---
name: Compliance & directive audits
slug: compliance-directive-audits
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
sources_digest: cd4fd2898a7d0313410d50856f984120dd4bf2bda61423302e01aa7866422db7
links:
  - to: operator-escalation-notification
    relation: uses
    description: directive-staleness-watch notifies via telegram-notify.sh.
generator:
  version: 1
covers:
  - symbol: externals
    kind: function
    at: 'scripts/ops/context7-check.py:L59-L75'
  - symbol: scan
    kind: function
    at: 'scripts/ops/context7-check.py:L78-L108'
  - symbol: walk_calls
    kind: function
    at: 'scripts/ops/context7-check.py:L111-L122'
  - symbol: verdict
    kind: function
    at: 'scripts/ops/context7-check.py:L125-L138'
  - symbol: main
    kind: function
    at: 'scripts/ops/context7-check.py:L141-L170'
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

Watchers and sweepers that audit standing documentation and directive drift: directive-rule-sweep flags rules that exist only in ephemeral directives (verified by a zibberflux canary fixture), directive-staleness-watch alerts on PENDING directives past a threshold, and context7-check detects external-library imports without a prior Context7 call. All are advisory — they report to logs/Telegram, never block or edit.

## Related

- uses [[operator-escalation-notification]] — directive-staleness-watch notifies via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
