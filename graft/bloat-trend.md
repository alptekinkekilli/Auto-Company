---
name: bloat-trend
slug: bloat-trend
type: file
sources:
  - path: scripts/ops/bloat-trend.py
    hash: f74441749dee8335f3eb7b9fa4626fcde6b9903cf0006019a261e8c35115fe26
sources_digest: 3e232ea381ef4bec4947e6f0531d443f974034d08c1e18e714de47abbc332a73
links:
  - to: telegram-notify
    relation: uses
    description: Sends trend alerts via the shared Telegram script.
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

Trend watcher for per-cycle turn-economy metrics. Ingests audit lines into durable NDJSON history keyed by session id, compares sliding window (15 cycles) vs preceding. Alerts only on regression (p90 turns ≥20% worse AND bloated share doubled), target met (bloated ≤10% AND p90 ≤55 for two consecutive windows), or --report. Stored verdicts recomputed from raw numbers with current thresholds (thresholds changed 2026-08-02).

## Related

- uses [[telegram-notify]] — Sends trend alerts via the shared Telegram script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
