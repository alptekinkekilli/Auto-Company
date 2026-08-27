---
name: Turn-economy trend watcher
slug: turn-economy-trend-watcher
type: system
sources:
  - path: scripts/ops/bloat-trend.py
    hash: f74441749dee8335f3eb7b9fa4626fcde6b9903cf0006019a261e8c35115fe26
sources_digest: 3e232ea381ef4bec4947e6f0531d443f974034d08c1e18e714de47abbc332a73
links:
  - to: auto-company-loop-core
    relation: uses
    description: Ingests audit lines from auto-loop.log.
  - to: telegram-notification
    relation: uses
    description: Sends trend alerts via telegram-notify.sh.
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
---
<!-- context:generated:start -->
## Summary

Trend watcher answering whether per-cycle turn-economy metrics are improving over time, complementing the per-cycle verdicts from the auto-loop. Folds audit lines idempotently into a durable NDJSON history keyed by session id, then compares a sliding window against the preceding window. Recomputes stored verdicts from raw numbers using current thresholds (which changed on 2026-08-02) so comparisons measure cycles, not the ruler. Alerts only on regression, target met (two consecutive windows), or explicit --report.

## Related

- uses [[auto-company-loop-core]] — Ingests audit lines from auto-loop.log.
- uses [[telegram-notification]] — Sends trend alerts via telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
