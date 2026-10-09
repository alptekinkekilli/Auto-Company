---
name: Turn-economy & compliance watchers
slug: turn-economy-compliance-watchers
type: system
sources:
  - path: scripts/ops/bloat-trend.py
    hash: f74441749dee8335f3eb7b9fa4626fcde6b9903cf0006019a261e8c35115fe26
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
sources_digest: 40e277fb6f3746592e7b31a026c53e76bd26efc483c1458b2568e7e1097b1dae
links:
  - to: operator-notification-routing
    relation: uses
    description: >-
      bloat-trend sends Telegram alerts via telegram-notify.sh using runtime.env
      credentials.
generator:
  version: 1
covers:
  - symbol: ingest
    kind: function
    at: 'scripts/ops/bloat-trend.py:L54-L97'
  - symbol: is_bloated
    kind: function
    at: 'scripts/ops/bloat-trend.py:L109-L110'
  - symbol: summarise
    kind: function
    at: 'scripts/ops/bloat-trend.py:L113-L126'
  - symbol: pct
    kind: function
    at: 'scripts/ops/bloat-trend.py:L117-L118'
  - symbol: notify
    kind: function
    at: 'scripts/ops/bloat-trend.py:L129-L142'
  - symbol: fmt
    kind: function
    at: 'scripts/ops/bloat-trend.py:L145-L155'
  - symbol: d
    kind: function
    at: 'scripts/ops/bloat-trend.py:L146-L151'
  - symbol: main
    kind: function
    at: 'scripts/ops/bloat-trend.py:L158-L237'
  - symbol: hits_target
    kind: function
    at: 'scripts/ops/bloat-trend.py:L185-L187'
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
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
---
<!-- context:generated:start -->
## Summary

Operational watchers that measure and police cycle behavior. bloat-trend.py folds per-cycle turn-audit lines into durable NDJSON history and alerts only on regression (p90 turns +20% and bloated share doubling), target met (two consecutive windows), or explicit --report, recomputing stored verdicts from raw numbers with current thresholds so comparisons measure cycles, not the ruler. context7-check.py inspects cycle ndjson logs to detect code importing external libraries without first calling Context7, deliberately avoiding prefiltering on exact JSON strings (which caused silent false negatives). idle-skip-note.py records model-free idle-skip events as one auditable line per day.

## Related

- uses [[operator-notification-routing]] — bloat-trend sends Telegram alerts via telegram-notify.sh using runtime.env credentials.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
