---
name: Directive governance watchers
slug: directive-governance-watchers
type: system
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
  - path: scripts/ops/directive-staleness-watch.py
    hash: 6597a8a3666b54131d1b782a8d8ee308e705e33dbed83429da857f9b1f0360fd
  - path: scripts/ops/ledger-guard.py
    hash: 9892f74da9b9b06f9977b053a05717c67eeafc4030ee7dbd2e2bc087fb8c3400
sources_digest: 2959d95d54f727706244ee12b90ea7d17856b904afeace60b204011b1b0cdd01
links:
  - to: human-directive-writer
    relation: validates
    description: >-
      Sweep and staleness watchers audit the directive written by
      directive_writer.py.
  - to: telegram-notification-channel
    relation: uses
    description: Staleness watcher sends alerts via telegram-notify.sh.
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
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/ledger-guard.py:L43-L48'
  - symbol: _env_float
    kind: function
    at: 'scripts/ops/ledger-guard.py:L51-L55'
  - symbol: _app
    kind: function
    at: 'scripts/ops/ledger-guard.py:L58-L59'
  - symbol: _find_ledger
    kind: function
    at: 'scripts/ops/ledger-guard.py:L62-L69'
  - symbol: _metrics
    kind: function
    at: 'scripts/ops/ledger-guard.py:L72-L84'
  - symbol: _backup
    kind: function
    at: 'scripts/ops/ledger-guard.py:L87-L101'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/ledger-guard.py:L104-L108'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/ledger-guard.py:L111-L118'
  - symbol: _check
    kind: function
    at: 'scripts/ops/ledger-guard.py:L121-L146'
  - symbol: main
    kind: function
    at: 'scripts/ops/ledger-guard.py:L149-L212'
---
<!-- context:generated:start -->
## Summary

Three scripts guarding directive integrity: directive-rule-sweep.py audits which rule-like statements exist only in ephemeral directive files and are not backed by standing documentation, using a canary fixture (zibberflux marker) to verify the heuristic still works and exiting 3 if the canary isn't flagged or the live directive can't be read; directive-staleness-watch.py alerts when the directive stays PENDING beyond a threshold (only satisfiable by market evidence or explicit terminal decision), persisting last_notified to avoid spamming a 15-min cron; ledger-guard.py is a post-cycle integrity guard for the Gate-0 conflict ledger and consensus.md, doing rolling backups and loss detection against previous-cycle metrics, always exiting 0 (informational only).

## Related

- validates [[human-directive-writer]] — Sweep and staleness watchers audit the directive written by directive_writer.py.
- uses [[telegram-notification-channel]] — Staleness watcher sends alerts via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
